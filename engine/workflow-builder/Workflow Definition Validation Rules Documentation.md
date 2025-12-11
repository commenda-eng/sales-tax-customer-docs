# Workflow Definition Validation Rules Documentation

## GRAPH Rules (Topology/Structure)

These rules validate the workflow graph structure and topology.

#### 1\. GRAPH\_EXACTLY\_ONE\_START

Rule: Workflow must have exactly 1 START step  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Counts START steps; fails if count ≠ 1

#### 2\. GRAPH\_EXACTLY\_ONE\_END

Rule: Workflow must have exactly 1 END step  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Counts END steps; fails if count ≠ 1

#### 3\. START\_STEP\_NO\_INCOMING

Rule: START step must not have any incoming transitions  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Checks incoming transitions for START steps

#### 4\. END\_STEP\_SINGLE\_INCOMING

Rule: END step must have exactly 1 incoming transition  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Checks incoming count for END steps

#### 5\. END\_STEP\_NO\_OUTGOING

Rule: END step must not have outgoing transitions  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Checks outgoing transitions for END steps

#### 6\. TRANSITIONS\_UNIQUE

Rule: No duplicate (from, to) transition pairs  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Ensures no duplicate (fromStepId, toStepId) pairs

#### 7\. NO\_SELF\_LOOPS

Rule: Self-loop transitions are not allowed  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Checks that fromStepId \!== toStepId for all transitions

#### 8\. NO\_ISOLATED\_STEPS

Rule: Steps with no incoming or outgoing transitions are isolated  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Checks for steps (excluding START/END) with 0 incoming and 0 outgoing

#### 9\. ONLY\_SPLIT\_GATEWAY\_CAN\_FAN\_OUT

Rule: Only split gateways (parallel, exclusive, inclusive) may have more than one outgoing transition  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Non-split gateway steps cannot have \>1 outgoing transitions

#### 10\. JOIN\_GATEWAY\_MANY\_IN\_SINGLE\_OUT

Rule: Join gateway must have at least 2 incoming transitions and exactly 1 outgoing transition  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Applies to GATEWAY\_PARALLEL\_JOIN steps

#### 11\. CONDITIONAL\_SPLIT\_SINGLE\_DEFAULT

Rule: Conditional split gateway must have exactly 1 default transition  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Applies to GATEWAY\_EXCLUSIVE\_SPLIT and GATEWAY\_INCLUSIVE\_SPLIT

#### 12\. EXCLUSIVE\_SPLIT\_TWO\_OUTGOING

Rule: Exclusive gateway must have exactly 2 outgoing transitions (1 default, 1 conditional)  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Applies to GATEWAY\_EXCLUSIVE\_SPLIT steps

#### 13\. ONLY\_EXCLUSIVE\_INCLUSIVE\_STEP\_HAVE\_CONDITION

Rule: Regular steps cannot have conditional transitions  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: Only exclusive/inclusive split gateways can have conditional transitions

#### 14\. MISSING\_BATCH\_ITERATOR

Rule: Batch workflow should have an iterator  
Severity: ERROR  
Error Code: GRAPH\_INVALID  
Validation: BATCH mode sub-workflow steps must have an iterable property

## ID Rules

These rules ensure unique identifiers across workflow entities.

#### 1\. STEP\_IDS\_UNIQUE

Rule: Step IDs must be unique  
Severity: ERROR  
Error Code: ID\_INVALID  
Validation: Ensures no duplicate step IDs in the workflow

#### 2\. TRANSITION\_IDS\_UNIQUE

Rule: Transition IDs must be unique  
Severity: ERROR  
Error Code: ID\_INVALID  
Validation: Ensures no duplicate transition IDs

#### 3\. STEP\_GROUP\_IDS\_UNIQUE

Rule: Step group IDs must be unique  
Severity: ERROR  
Error Code: ID\_INVALID  
Validation: Ensures no duplicate step group IDs

## GROUP Rules

These rules validate step grouping and organization.

#### 1\. NO\_GROUP\_FOR\_SPECIAL\_NODES

Rule: Start/end/gateways cannot be grouped  
Severity: ERROR  
Error Code: GROUPING\_INVALID  
Validation: Only human nodes and system nodes can be grouped; START, END, and gateway steps cannot

#### 2\. GROUP\_STEP\_IDS\_EXISTS

Rule: Step group contains stepIds that do not reference existing steps  
Severity: ERROR  
Error Code: GROUPING\_INVALID  
Validation: All stepIds in a stepGroup must reference existing steps

#### 3\. STEP\_BELONGS\_TO\_ONLY\_ONE\_GROUP

Rule: Step ID belongs to multiple groups. Each step can only belong to one group  
Severity: ERROR  
Error Code: GROUPING\_INVALID  
Validation: Ensures each step appears in at most one stepGroup

#### 4\. STEP\_GROUP\_CANNOT\_BE\_EMPTY

Rule: Step group cannot be empty. Each step group must contain at least one step  
Severity: ERROR  
Error Code: GROUPING\_INVALID  
Validation: Each stepGroup must have at least one stepId

#### 5\. LEGACY\_SERVICE\_REQUEST\_REQUIRES\_STEP\_GROUPS

Rule: Workflow with legacyServiceRequestType must have at least one step group  
Severity: ERROR  
Error Code: GROUPING\_INVALID  
Validation: If legacyServiceRequestType is set, at least one stepGroup must exist

## LEGACY\_SERVICE\_REQUEST Rules

These rules validate legacy service request mappings and compatibility.

#### 1\. LEGACY\_SERVICE\_REQUEST\_TYPE\_GROUP\_TASK\_UNIQUE

Rule: Multiple steps share the same legacy combination (serviceRequestType, taskGroup, taskKey)  
Severity: ERROR  
Error Code: LEGACY\_CONFIG\_INVALID  
Validation: The tuple (serviceRequestType, taskGroupKey, taskKey) must be unique across all steps

#### 2\. LEGACY\_SERVICE\_REQUEST\_TASK\_GROUP\_EXISTS\_IN\_TEMPLATE

Rule: Step group with legacyServiceRequestTaskGroupKey does not exist in serviceRequestTemplate  
Severity: ERROR  
Error Code: LEGACY\_CONFIG\_INVALID  
Validation: StepGroups with legacyServiceRequestTaskGroupKey must exist in the service request template

#### 3\. LEGACY\_SERVICE\_REQUEST\_TASK\_EXISTS\_IN\_TEMPLATE

Rule: Step with legacyServiceRequestTaskKey does not exist in the corresponding taskGroup template  
Severity: ERROR  
Error Code: LEGACY\_CONFIG\_INVALID  
Validation: Steps with legacyServiceRequestTaskKey must exist in the corresponding taskGroup's tasks in the template

#### 4\. LEGACY\_SERVICE\_REQUEST\_TASK\_ONLY\_ON\_HUMAN\_STEP

Rule: Only human steps can have legacyServiceRequestTask mapping  
Severity: ERROR  
Error Code: LEGACY\_CONFIG\_INVALID  
Validation: Only human node types can have legacyServiceRequestTaskKey set  
