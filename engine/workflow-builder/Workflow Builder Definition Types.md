# Workflow Builder Definition

### TWorkflowDefinition

* name \- name of this workflow  
* steps \- steps involved in the workflow  
* stepTransitions \- stores transitions between the steps  
* stepGroups \- stores all the stepGroups which is just for a UI wrapper around the tasks.  
* legacyServiceRequestType \-  maps to the service request type.

```ts
export type TWorkflowDefinition = {
  id: string;
  name: string;
  steps: TWorkflowStepDefinition[];
  stepTransitions: TWorkflowStepTransition[];
  stepGroups?: TStepGroup[];
  legacyServiceRequestType?: string;
};

```

### TWorkflowStepDefintion

#### WorkflowStepType

* **start** — The entry point of the workflow. Each workflow must have exactly one start node.  
* **end** — The terminal node of the workflow. A workflow must have exactly one end node.  
* **human**.\* — Represents a step that requires human input.  
  * human.url\_redirect — Redirects a user to a specific URL. // Not implemented  
  * human.form — Presents a structured form to collect data. // Not implemented  
  * human.confirm — Waits for user confirmation or acknowledgment.  
  * human.doc\_upload — Requests a user to upload one or more documents. // Not implemented  
* **sys.sub\_workflow** — A system step that invokes another workflow, either in single execution mode or in batch (iterative) mode.  
* **gateway**.\* — A logical control-flow node used for routing execution.  
  * gateway.parallel\_split — Triggers multiple branches to run in parallel.  
  * gateway.parallel\_join — Waits for all incoming branches to complete before proceeding.  
  * gateway.exclusive\_split — Chooses exactly one outgoing path based on evaluated conditions. Condition is required only in one of the paths.  
  * gateway.inclusive\_split — Can trigger multiple outgoing branches if their conditions evaluate to true.

#### TWorkflowBaseStepDefinition

* **id** — A unique identifier for the step within the workflow.  
* **type** — The type of step, one of the WorkflowStepType values.  
* **name** — A human-readable label shown in the UI and logs.  
* **outputSchema** — An optional JSON Schema describing the expected structure of the step’s output. This is primarily used for validation and for tooling to infer available data fields.  
* **group** — Optional grouping metadata for UI organization. It includes:  
  * groupId — Identifier for the logical group this step belongs to.  
  * order — The relative position of this step within the group.  
* **legacyServiceRequestTaskKey** — A backward-compatibility field linking this step to older service-request tasks.  
* **activationPolicy** — An optional policy that defines the default runtime activation state for this step.  
* **ui** — Contains UI metadata for the workflow designer, especially React Flow coordinates:  
  * reactFlow.position.x and .y — The step’s position in the visual editor canvas.

```ts
export type TWorkflowBaseStepDefinition = {
  id: string;
  type: WorkflowStepType;
  name: string;
  outputSchema?: Record<string, any>;
  group?: {
    groupId: string;
    order: number;
  };
  legacyServiceRequestTaskKey?: string;
  activationPolicy?: TStepActivationPolicy;
  ui: {
    reactFlow: {
      position: {
        x: number;
        y: number;
      };
    };
  };
};
```

#### TStepActivationPolicy

* **defaultStatus**: defines what the default status of the step should be while starting the step.


```ts
export type TStepActivationPolicy = {
  defaultStatus?: WorkflowRuntimeStepStatus;
};
```

#### TBaseSubWorkflowStepDefinition

* **mode** — Defines whether the subworkflow runs once (SINGLE) or for each item in a collection (BATCH).  
* **childWorkflowTemplateVersionId** — References the versioned child workflow template to execute.  
* **dataSources** — A list of data source calls that can be executed before the subworkflow starts. These provide access to external data that can be used within the step’s execution.  
* **inputMapping** — A list of mappings that define how parent child workflows context will be generated.  
* **contextProjection** — Similar to inputMapping, but in the opposite direction — defines how outputs from the child workflow are written back into the parent workflow. // Not used anywhere  
* **childWorkflowName** — A JSONata expression used to dynamically name the spawned child workflows. If not provided, the system defaults to the child workflow’s template name.  
* **iterable** — Defines how the batch is constructed — typically by evaluating a JSONata expression that returns an array. It is only used with BatchSubWorkflows.

```ts
export type TBaseSubWorkflowStepDefinition = TWorkflowBaseStepDefinition & {
  type: WorkflowStepType.SYS_SUB_WORKFLOW;
  mode: SubWorkflowStepMode;
  childWorkflowTemplateVersionId: string;
  dataSources?: TDataSourceCall[];
  inputMapping?: TMapping[];
  contextProjection?: TMapping[];
  childWorkflowName?: TExpr;
};

export type TSingleWorkflowStepDefinition = TBaseSubWorkflowStepDefinition & {
  mode: SubWorkflowStepMode.SINGLE;
};

export type TBatchWorkflowStepDefinition = TBaseSubWorkflowStepDefinition & {
  mode: SubWorkflowStepMode.BATCH;
  iterable: TIterableProvider;
};

export type TSubWorkflowStepDefinition =
  | TSingleWorkflowStepDefinition
  | TBatchWorkflowStepDefinition;
```

#### Other Step type definitions :-

```ts
export type TStartWorkflowStepDefinition = TWorkflowBaseStepDefinition & {
  type: WorkflowStepType.START;
};

export type TEndWorkflowStepDefinition = TWorkflowBaseStepDefinition & {
  type: WorkflowStepType.END;
};

export type TBaseHumanStepDefinition = TWorkflowBaseStepDefinition & {
  type:
    | WorkflowStepType.HUMAN_URL_REDIRECT
    | WorkflowStepType.HUMAN_FORM
    | WorkflowStepType.HUMAN_CONFIRM
    | WorkflowStepType.HUMAN_DOC_UPLOAD;
  // assignee: string;
};

export type TBaseGatewayStepDefinition = TWorkflowBaseStepDefinition & {
  type:
    | WorkflowStepType.GATEWAY_PARALLEL_SPLIT
    | WorkflowStepType.GATEWAY_PARALLEL_JOIN
    | WorkflowStepType.GATEWAY_EXCLUSIVE_SPLIT
    | WorkflowStepType.GATEWAY_INCLUSIVE_SPLIT;
};

export type TWorkflowStepDefinition =
  | TWorkflowBaseStepDefinition
  | TSingleWorkflowStepDefinition
  | TBatchWorkflowStepDefinition
  | TStartWorkflowStepDefinition
  | TEndWorkflowStepDefinition
  | TBaseHumanStepDefinition
  | TBaseGatewayStepDefinition;
```

### TStepTransition

* **fromStepId** — The step where this transition originates.  
* **toStepId** — The target step to be activated if the transition passes.  
* **condition** — An optional JSONata expression (TExpr) that evaluates to a boolean value. If true, this transition is followed.  
* **isDefault** — Marks this transition as the default branch, used in exclusive gateways when no other condition is met.  
* **label** — Optional human-readable name or description for the edge (used in visual editors).  
* **onArrival** — Allows setting some configurations like status for the arriving step.  
* **ui.reactFlow.handle** — Visual metadata describing which handles (source/target anchors) this edge connects in the diagram editor.

```ts
export type TWorkflowStepTransition = {
  id: string;
  fromStepId: string;
  toStepId: string;
  condition?: TExpr;
  isDefault?: boolean;
  label?: string;
  onArrival?: TStepTransitionOnArrival;
  ui: {
    reactFlow: {
      handle: {
        sourceHandle: string;
        targetHandle: string;
      };
    };
  };
};

```

#### TStepTransitionOnArrival

For example, if the issue is reported from a step, the next step should be action required.

```ts
export type TStepTransitionOnArrival = {
  // Step status when this transition activates the target step
  status?: WorkflowRuntimeStepStatus;
};
```

