# Workflow Runtime Types

### WorkflowRuntimeStatus

* **NOT\_STARTED** — The workflow is defined but has not yet begun execution.  
* **IN\_PROGRESS** — The workflow is actively executing one or more steps.  
* **COMPLETED** — All steps have finished successfully.  
* **FAILED** — One or more steps have failed and the workflow cannot continue.  
* **CANCELLED** — Execution was explicitly cancelled.

### TRuntimeWorkflowExecution

* **rootWorkflowExecutionId**: The root workflow, if child workflows trigger more child workflows.  
* **parentWorkflowExecutionId**: References the execution ID of a parent workflow, if this instance was spawned as a subworkflow.  
* **workflowTemplateVersionId**: Identifies which version of the workflow template was used to start this execution.  
* **runtimeStatus**: The current overall status of this workflow instance.  
* **startedAt / completedAt / failedAt**  
* **lastActivityAt** \- Currently we only track when a step is updated.  
* **context \-** stores some additional information about the workflow. Eg:- For a DSC Incorporation workflow, it would store directorId. It also acts like the global context of the workflow. “**\_\_context\_\_**” refers to the global context.  
* **steps**: An object of step execution states, keyed by the step execution id. Each state is a TRuntimeWorkflowStepExecution object.

```ts
export type TRuntimeWorkflowExecution = {
  id: string;
  correlationId: string;
  parentWorkflowExecutionId?: string;
  workflowTemplateVersionId: string;
  runtimeStatus: WorkflowRuntimeStatus;
  startedAt: string;
  completedAt?: string;
  failedAt?: string;
  lastActivityAt?: string;
  context: Record<string, any>;
  steps: Record<string, TRuntimeWorkflowStepExecution>;
};
```

### WorkflowRuntimeStepStatus

* **NOT\_STARTED** \- The step has not started till now.  
* **IN\_PROGRESS** \- The step is in progress.  
* **COMPLETED** \- The step is completed now.  
* **DISABLED** \- The step is currently disabled.  
* **FAILED** \- The step failed.

```ts
export enum WorkflowRuntimeStepStatus {
  NOT_STARTED = "NotStarted",
  IN_PROGRESS = "InProgress",
  COMPLETED = "Completed",
  DISABLED = "Disabled",
  FAILED = "Failed"
}
```

### 

### TRuntimeWorkflowExecution

type \- the step type  
stepId \- this is id from the definition  
status \- the runtime status of the step  
startedAt, completedAt, failedAt \- when the step was started, completed or failed  
dueAt \- due date for this step  
outputData \- the step’s output following the output schema.  
childWorkflowExecutions \- all child workflows triggered in this step.

```ts
export type TRuntimeWorkflowStepExecution = {
  id: string;
  type: WorkflowStepType;
  stepId: string;
  status: WorkflowRuntimeStepStatus;
  attempt: number;
  startedAt?: string;
  completedAt?: string;
  failedAt?: string;
  dueAt?: string;
  outputData?: Record<string, any>; // following the outputSchema
  childWorkflowExecutions?: { id: string }[];
};
```

