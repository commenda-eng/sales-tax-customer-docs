# Workflow Step Types

### **START**

This marks the **beginning of the workflow**. There should be exactly one start step in a workflow.

### **END**

This marks **the final point** of the workflow. When the workflow reaches this step, all work for that execution is complete.

### **HUMAN\_CONFIRM**

This step means a human just confirms that a step is completed or not before the workflow can continue.  
Example: Waiting till the agent files in MCA and marks the step as completed.

### **SYS\_SUB\_WORKFLOW**

This step triggers another workflow inside the current workflow. It’s like saying, “Run this small process and come back when it’s done.” The system handles this automatically—no human action required. You can trigger a single and a batch of similar workflows.  
Example: We would want to trigger multiple DSC workflows from an India Private Incorporation Workflow.

### **GATEWAY\_PARALLEL\_SPLIT**

This step tells the workflow to branch into multiple paths at the same time.  
All the branches start together, in parallel.

### **GATEWAY\_PARALLEL\_JOIN**

This step waits for all parallel branches to finish before moving forward.  
Think of it like: “We’ll continue only after everything running in parallel is completed.”

### **GATEWAY\_BOOLEAN\_EXCLUSIVE\_SPLIT**

This is a yes/no decision point in the workflow.  
Only one path will be taken depending on the answer.

### **GATEWAY\_INCLUSIVE\_SPLIT**

This step allows the workflow to choose multiple paths based on conditions, not just one.  
It’s flexible—one or many paths may be taken depending on the data.  
Example:  
If the user is new → send onboarding.  
If the user is premium → send perks.  
If both conditions are true → do both.

