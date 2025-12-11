# Rendering Service Request UI

*Note:- The given method is just a temporary solution till we have a fully functional workflow powered by form builder. This is just for powering our existing service requests orchestration using workflows. **JUST ORCHESTRATION**. Other business contexts like files, assigneeType, workRequest, corporation, company etc still lie inside the serviceRequest.*

For each **service request type**, we maintain a configuration that defines:

* Which **task groups** exist  
* Which **tasks** belong to each group

We represent these using a TaskGroup enum and a Task enum.

At runtime, we use this configuration to generate the **service request instances** on the backend.

On the frontend, we have a componentMap that maps each taskKey to a React component, which is then rendered.  
 Examples of common components include:

* AddBankAccount  
* MarkAsCompleted

## Workflow Executions As Source of Truth

Whenever a service request is initiated, we try to start a **workflow execution** for it.

* A workflow execution is started **only if** there is a workflow link associated with that service request type.  
* If a workflow execution exists, it becomes the **source of truth** for task statuses.

Ideally, we would render the service request UI **directly** from the workflow execution and remove the separate service request model. However, this is not currently possible because there is additional business context attached to the service request that workflows don’t know about (e.g. files, agentFirms, subsidiaries, corporations, etc.).

As a result:

* We will have **service request runtime instances** and **workflow execution runtime instances** co-existing.  
* These two must be **kept in sync**.  
* **Statuses** should always come from the workflow execution.

## Syncing Task Updates

Every time we update a task in the service request:

1. If the service request has an associated workflow execution, we **propagate the update** to the workflow execution.  
2. We wait for that update to complete and then **fetch the latest runtime statuses** from the workflow.  
3. We iterate over the new statuses and build the corresponding Prisma mutations.  
4. We execute those updates inside a **transaction**.

If something fails midway (e.g. while creating or applying all mutations), we provide a **manual “Sync” button** that can be used to reconcile statuses between the service request and the workflow.

## Mapping Workflows to Service Requests

When creating a new workflow, you will have the option to **connect it to a service request**:

* At the workflow level, we have a legacyServiceRequestKey.  
* Within a workflow, you can create **stepGroups**.  
* These stepGroups can be linked to existing taskGroups from the service request model.

The mapping flow looks like this:

1. **Select** the legacyServiceRequestKey.  
2. **Select** the taskGroup for each stepGroup.  
3. For each step, **select** the taskKey.

Once this mapping is complete:

* If a UI component exists for a given taskKey in componentMap, that custom component will be rendered.  
* If no matching component is found, we render a **Generic Task**:  
  * It is assigned to an agent.  
  * It behaves as a “Mark as Completed” task.

This means:

* Any new task groups or tasks you add in the workflow that **do not** map 1:1 to existing service request tasks will fall back to the **Generic Task** UI.

## 

## Handling Dynamic DSC Task Groups for India Pvt Ltd

The India Pvt Ltd incorporation workflow requires dynamic task groups: each director who does not already have a DSC must go through a separate DSC onboarding flow.

This creates a domain mismatch:

* In the **Workflow domain**, DSC onboarding is represented as one child workflow per director.  
* In the **Service Request domain**, each DSC workflow must appear as a separate task group.

We do not yet know whether this pattern generalizes to all future workflows (child-of-child workflows, multiple step groups, etc.), so we implement a targeted, DSC-specific solution that can evolve later.

We do the following right now :- 

* Identifies DSC-related child workflow executions.  
* Creates or updates corresponding Service Request task groups.  
* Links each task group to the correct workflow execution (`workflowExecutionId`).  
* Ensures the group name and ordering follow the SR UI conventions.

When the UI updates a task, we determine which workflow execution to update:

```ts
workflowExecutionToUpdate =
    serviceRequestTaskGroup.workflowExecutionId
        OR serviceRequest.workflowExecutionId
```

If the task belongs to a DSC group, we update the **child workflow execution**.  
Otherwise, we update the **parent workflow execution**.

## Why We Are Not Generalizing Yet

* Should all child workflows appear as Service Request task groups?  
* Should child-of-child workflows be shown?  
* How should workflows with multiple step groups be projected?  
* Should we introduce a generic “projection type” system?

We will revisit these once more diverse workflows are built and real patterns emerge.

