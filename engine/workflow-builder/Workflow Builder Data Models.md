# Workflow Data Models

All of this is in commenda-logical-backend. 

## Workflow Templates

This model stores a workflow template. 

```ts
model WorkflowTemplate {
  id          String  @id @default(cuid())
  name        String
  description String?

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  ActiveVersion   WorkflowTemplateVersion? @relation(fields: [activeVersionId], references: [id], name: "active_workflow_template_version")
  activeVersionId String?                  @unique

  Versions WorkflowTemplateVersion[] @relation("workflow_template_has_version")

  WorkflowTemplateLinks WorkflowTemplateLink[]
}

```

## Workflow Template Versions

This model stores multiple versions of a particular template. The templates are initially created in Draft status. Only one WorkflowTemplateVersion can be linked to the workflow as the currently-active version. 

// Let’s add details here explaining how VersionStatus and ActiveWorkflowTemplate interact and exactly what each one means. 

```ts
enum WorkflowTemplateVersionStatus {
  DRAFT
  PUBLISHED
  DEPRECATED
}

model WorkflowTemplateVersion {
  id String @id @default(cuid())

  WorkflowTemplate   WorkflowTemplate @relation(fields: [workflowTemplateId], references: [id], onDelete: Cascade, name: "workflow_template_has_version")
  workflowTemplateId String

  version     String // Semantic version: "1.0.0"
  versionNote String? // Changelog for this version

  definition Json

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  status WorkflowTemplateVersionStatus @default(DRAFT)

  // This will be filled, if this is the active version of the workflow.
  ActiveWorkflowTemplate WorkflowTemplate? @relation(name: "active_workflow_template_version")

  WorkflowExecutions WorkflowExecution[]

  @@unique([workflowTemplateId, version])
}

```

## Workflow Links

Workflow Link tells how a workflow should be triggered. There are two types of links currently.  
SERVICE\_CATALOG \- If you want to link it to a specific type of service request.   
PRODUCT \- If you want to link to a product from our billing software (currently Chargebee).

So if any service request or a product is bought and a workflow link is present, an instance of the active workflow template for that workflow will be created by calling the TemporalWorkflowService API. 

```ts
enum WorkflowLinkType {
  SERVICE_CATALOG
  PRODUCT
}
model WorkflowTemplateLink {
  id String @id @default(cuid())

  WorkflowTemplate   WorkflowTemplate @relation(fields: [workflowTemplateId], references: [id], onDelete: Cascade)
  workflowTemplateId String

  entityType WorkflowLinkType
  entityId   String

  @@unique([entityType, entityId])
}
```

## Workflow Executions

This is a running instance of a workflow template version, corresponding to a specific service that is being delivered for a customer or a subworkflow thereof. The actual runtime state of this execution gets tracked in temporal.

Each workflow instance is in one of the following statuses: 

* CREATED \- The instance was created and hasn’t started to run.  
* STARTED \- The execution of the workflow has started.  
* FAILED\_TO\_START \- The execution failed to start.  
* COMPLETED \- workflow execution completed successfully.  
* FAILED \- workflow execution failed.

In the data model,

* **workflowTemplateVersionId** \- refers to the template version used for execution.  
* **parentWorkflowExecutionId** \- If this is the child execution, it will refer to the workflowExecution that triggered it.  
* **rootWorkflowExecutionId** \- tracks the root workflow that eventually triggered this execution. Can be used for correlation of related requests.   
* **context** \- the additional data about this workflow execution. Like directorID, if DSC.  
  * Within the temporal execution engine this is not used. It’s just metadata stored in the global context of the request, which the caller can use.   
  * Not currently getting used for anything.  
* **ServiceRequest** \- The service request associated with this execution  
* **ServiceRequestTaskGroup** \- task groups like DSC are also treated as child workflow execution.

```ts

enum WorkflowExecutionStatus {
  CREATED
  STARTED
  FAILED_TO_START
  COMPLETED
}

// Running instance of a workflow template
model WorkflowExecution {
  id String @id @default(cuid())

  name String

  WorkflowTemplateVersion   WorkflowTemplateVersion @relation(fields: [workflowTemplateVersionId], references: [id])
  workflowTemplateVersionId String

  createdAt DateTime @default(now())

  ParentWorkflowExecution   WorkflowExecution? @relation(fields: [parentWorkflowExecutionId], references: [id], onDelete: Cascade, name: "parent_workflow_execution")
  parentWorkflowExecutionId String?

rootWorkflowExecutionId String?
  RootWorkflowExecution   WorkflowExecution? @relation(fields: [rootWorkflowExecutionId], references: [id], onDelete: Cascade, name: "root_workflow_execution")

  context       Json?
  // This is not the runtime status of the workflow execution.
  status        WorkflowExecutionStatus @default(CREATED)

  ChildWorkflowExecutions WorkflowExecution[] @relation("parent_workflow_execution")

DescendantWorkflowExecutionsFromRoot WorkflowExecution[] @relation("root_workflow_execution")

  ServiceRequest          ServiceRequest?
  ServiceRequestTaskGroup ServiceRequestTaskGroup?
}

```

