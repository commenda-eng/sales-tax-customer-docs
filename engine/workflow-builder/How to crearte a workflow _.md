# How to create a workflow ?

### **1\. Accessing Workflow Management**

* Go to the **Admin Portal**.  
* On the left sidebar, scroll to the bottom and click **Workflow Management**.  
* You’ll land on a page that lists all existing workflows.  
* On the top right, you’ll see two tabs:  
  * **Workflow Links**  
  * **Create Workflow**

### **2\. Creating a New Workflow Template**

1. Click Create Workflow.  
2. A modal appears where you can enter:  
   * Workflow name  
   * Other optional fields  
3. Click Create to add the new workflow.  
4. The new workflow will now appear in the workflows table.

### **3\. Opening an Existing Workflow**

* Click any row in the workflow list.  
* This opens the Workflow Detail Page for that template.  
* Here you’ll see all existing versions for that workflow.  
* For a newly created workflow, this section will be empty.

### **4\. Creating a Version**

1. On the workflow detail page, click Add Version (top right).  
2. A modal appears asking for:  
   * Version number  
   * Starter version (optional)  
     * This lets you start from an existing version instead of building from scratch.  
3. Click Create to generate the new version.  
4. The system opens the Workflow Editor.

### **5\. Using the Workflow Editor**

Inside the editor, you will see:

* A Steps Panel on the left, containing all available step types.  
* A central Canvas where you can drag and drop steps to build your workflow.  
* A Configuration Panel on the right that appears when you click any step.

#### **Important Notes**

* There is no autosave right now.  
* Save your progress frequently using the Save button on the top right.  
* When ready, click Publish.  
* Newly created versions start in Draft status.  
* Publishing makes the version eligible to be activated.

### **6\. Marking a Version as Active**

1. After publishing a version, return to the workflow’s versions list.  
2. You will see an Activate Version option next to published versions.  
3. Marking a version as active makes it the version used whenever this workflow is generated.

### **7\. Understanding Workflow Links**

Workflow links decide *how and when* a workflow is triggered.

To access links:

* Go back to the main workflow page.  
* Click the Workflow Links tab.

You’ll see a list of existing links. You can edit or delete these.

#### **Creating a Workflow Link**

1. Click Add Link.  
2. A modal will open where you must select:  
   * Workflow Template (dropdown of all templates)  
   * Link Type:  
     * Service Request Type  
     * Product ID  
   * Identifier:  
     * The exact service request type or product ID  
3. Save the link.

#### How Links Work

* When a matching service request is created, or a product with the specified ID is purchased, the system automatically triggers and generates the workflow.

