# Documentation Generation Plan for Workflow Builder

## Overview
This document provides a comprehensive plan for generating documentation from source .md files, including Mintlify's documentation system prompt and best practices for creating high-quality technical documentation.

---

## Mintlify Documentation System Prompt

### Core Principles

1. **Always prefer updating existing content over creating new content** - Search thoroughly for related documentation before creating new files
2. **Gather context first** - Always start by listing files and navigation structure to understand the existing documentation landscape
3. **Complete tasks fully** - Finish all documentation work autonomously without requiring feedback loops
4. **Follow existing conventions** - Match the style, structure, and patterns already present in the documentation
5. **ALWAYS PLAN YOUR TASKS** - Use task management to plan and track progress

### Standard Workflow

#### Step 1: Context Gathering (ALWAYS DO THIS FIRST)
Execute in parallel:
- List all existing files to see current documentation
- Read navigation structure to understand site organization

#### Step 2: Investigation
Based on the task:
- Read relevant existing files to understand current documentation
- Identify patterns in file naming, structure, and navigation paths
- Determine if content should be updated or created new
- Ask clarifying questions if necessary

#### Step 3: Content Decision
**Strongly prefer updating existing content:**
- If related documentation exists, update it rather than creating duplicates
- Only create new files when the content is genuinely new and distinct
- Check for partial matches - even tangentially related content should be updated rather than duplicated

#### Step 4: Implementation

**For Updates (preferred):**
1. Read the full file to understand context
2. Use edit with exact string matching (including whitespace)
3. Set `replaceAll: true` for multiple occurrences
4. Verify navigation items remain correct

**For New Content (only when necessary):**
1. Create file with write using relative paths
2. Include proper MDX frontmatter:
   ```yaml
   ---
   title: Clear, descriptive page title
   description: Concise summary for SEO/navigation
   ---
   ```
3. Modify the docs.json navigation object structure to add the new page
4. Follow existing path conventions and hierarchy

#### Step 5: Verification
After making changes:
- Re-run read_navigation if navigation was modified
- Ensure all files are properly linked in navigation

#### Step 6: Completion
After completing the task:
- If changes were made: A PR will be automatically created
- If no changes were made: Inform the user
- Always provide a clear, user-friendly summary
- Focus on outcomes, not process

### Content Standards

#### File Format
- All files are MDX with YAML frontmatter
- Follow exact formatting conventions present in existing files
- Match existing patterns for consistency

#### Writing Requirements
- Second-person voice ("you")
- Sentence case for all headings ("Getting started", not "Getting Started")
- Active voice and direct language
- Prerequisites at start of procedural content
- Language tags on all code blocks
- Alt text on all images
- Relative paths for internal links

#### Language Guidelines
- NO promotional language or marketing speak
- Be specific, not vague - cite sources when making claims
- Avoid excessive conjunctions (moreover, furthermore, additionally)
- No editorializing ("it's important to note")
- Use Lucide icon library for any icons

#### Technical Accuracy
- Test all code examples before including them
- Verify all external links
- Use precise version numbers and specifications
- Maintain consistent terminology throughout

#### Component Documentation
- Start with action-oriented language: "Use [component] to..."
- End all property descriptions with periods
- Use proper technical terminology ("boolean" not "bool")
- Keep code examples simple and practical

### Critical Rules

1. **Never make assumptions** - Read existing documentation to understand the technical domain
2. **Always complete tasks fully** - No TODOs or partial implementations unless explicitly requested
3. **Respect exact formatting** - When editing, match whitespace and formatting exactly
4. **Maintain navigation integrity** - Ensure all documentation is properly accessible
5. **Prioritize user success** - Document just enough for users to accomplish their goals

---

## Documentation Generation Workflow for Workflow Builder

### Phase 1: Discovery and Analysis

#### Step 1: Locate Source Files
```
Action: List all files in engine/workflow-builder directory
Expected: Find all 15 .md files
```

#### Step 2: Read All Source Files
```
Action: Read each .md file to understand:
- Content structure
- Topics covered
- Code examples
- Relationships between files
- Technical depth
```

#### Step 3: Analyze Existing Documentation
```
Action: Read engine/workflow-builder/overview.mdx
Purpose: Understand current documentation state
Check: What content already exists vs. what's new
```

#### Step 4: Review Navigation Structure
```
Action: Read navigation from docs.json
Purpose: Understand where Workflow Builder fits
Check: Current navigation hierarchy for workflow-builder
```

### Phase 2: Content Organization

#### Step 1: Categorize Content
Organize the 15 files into logical groups:

**Getting Started**
- Introduction/Overview
- Quickstart guides
- Basic concepts

**Core Concepts**
- Workflow fundamentals
- Triggers
- Actions
- Conditions
- Variables
- Data flow

**Advanced Topics**
- Complex workflows
- Error handling
- Performance optimization
- Best practices

**Reference**
- API documentation
- Configuration options
- Examples and templates

#### Step 2: Create Content Hierarchy
```
workflow-builder/
├── overview.mdx (update existing)
├── quickstart.mdx
├── concepts/
│   ├── workflows.mdx
│   ├── triggers.mdx
│   ├── actions.mdx
│   ├── conditions.mdx
│   └── variables.mdx
├── guides/
│   ├── creating-workflows.mdx
│   ├── testing-workflows.mdx
│   └── deploying-workflows.mdx
├── advanced/
│   ├── error-handling.mdx
│   ├── performance.mdx
│   └── best-practices.mdx
└── reference/
    ├── api.mdx
    ├── configuration.mdx
    └── examples.mdx
```

### Phase 3: Content Transformation

#### Step 1: Convert .md to .mdx
For each source file:

1. **Add YAML Frontmatter**
```yaml
---
title: [Descriptive title from content]
description: [1-2 sentence summary]
---
```

2. **Format Headings**
- Use sentence case
- Ensure proper hierarchy (h1 → h2 → h3)
- Make headings descriptive and scannable

3. **Enhance Code Blocks**
```javascript
// Add language tags
// Add comments for clarity
// Ensure examples are complete and runnable
```

4. **Add Callouts Where Appropriate**
```mdx
<Note>
Important information users should know
</Note>

<Warning>
Critical warnings about potential issues
</Warning>

<Tip>
Helpful tips for better results
</Tip>
```

5. **Structure Content**
- Start with brief introduction
- Add prerequisites if needed
- Use numbered steps for procedures
- Include examples after explanations
- End with next steps or related links

#### Step 2: Cross-Reference Content
- Link related pages together
- Create "See also" sections
- Reference API docs from guides
- Link examples to concepts

#### Step 3: Optimize for Clarity
- Break long paragraphs into shorter ones
- Use bullet points for lists
- Add tables for comparison data
- Include diagrams where helpful (describe in alt text)

### Phase 4: Navigation Integration

#### Update docs.json Navigation
```json
{
  "group": "Workflow Builder",
  "icon": "workflow",
  "pages": [
    "engine/workflow-builder/overview",
    "engine/workflow-builder/quickstart",
    {
      "group": "Core concepts",
      "pages": [
        "engine/workflow-builder/concepts/workflows",
        "engine/workflow-builder/concepts/triggers",
        "engine/workflow-builder/concepts/actions",
        "engine/workflow-builder/concepts/conditions",
        "engine/workflow-builder/concepts/variables"
      ]
    },
    {
      "group": "Guides",
      "pages": [
        "engine/workflow-builder/guides/creating-workflows",
        "engine/workflow-builder/guides/testing-workflows",
        "engine/workflow-builder/guides/deploying-workflows"
      ]
    },
    {
      "group": "Advanced",
      "pages": [
        "engine/workflow-builder/advanced/error-handling",
        "engine/workflow-builder/advanced/performance",
        "engine/workflow-builder/advanced/best-practices"
      ]
    },
    {
      "group": "Reference",
      "pages": [
        "engine/workflow-builder/reference/api",
        "engine/workflow-builder/reference/configuration",
        "engine/workflow-builder/reference/examples"
      ]
    }
  ]
}
```

### Phase 5: Quality Assurance

#### Content Checklist
- [ ] All files have proper frontmatter
- [ ] All headings use sentence case
- [ ] All code blocks have language tags
- [ ] All images have alt text
- [ ] All links are relative and working
- [ ] No marketing language
- [ ] Consistent terminology throughout
- [ ] Examples are complete and tested
- [ ] Prerequisites are listed
- [ ] Next steps are provided

#### Technical Checklist
- [ ] All files are valid MDX
- [ ] Navigation structure is correct
- [ ] File paths match navigation
- [ ] No broken internal links
- [ ] No duplicate content
- [ ] Proper hierarchy maintained

---

## Best Practices for Workflow Builder Documentation

### 1. Start with User Goals
- What does the user want to accomplish?
- What's the fastest path to success?
- What are common use cases?

### 2. Progressive Disclosure
- Start simple, add complexity gradually
- Quickstart → Concepts → Advanced
- Don't overwhelm beginners
- Provide depth for advanced users

### 3. Show, Don't Just Tell
```mdx
<!-- Bad -->
You can create a workflow with triggers.

<!-- Good -->
Create a workflow that sends a notification when a user signs up:

```javascript
const workflow = {
  trigger: 'user.signup',
  actions: [
    {
      type: 'notification',
      message: 'Welcome {{user.name}}!'
    }
  ]
}
```
```

### 4. Provide Context
- Explain WHY, not just HOW
- Show when to use different approaches
- Explain trade-offs and limitations

### 5. Use Consistent Patterns

**For Concepts:**
1. Brief definition
2. Why it matters
3. How it works
4. Simple example
5. Related concepts

**For Guides:**
1. What you'll build
2. Prerequisites
3. Step-by-step instructions
4. Verification steps
5. Next steps

**For Reference:**
1. Overview
2. Parameters/options table
3. Examples
4. Related references

### 6. Anticipate Questions
- What could go wrong?
- What are common mistakes?
- What are the limitations?
- How does this relate to other features?

### 7. Keep It Current
- Use current syntax and APIs
- Remove deprecated features
- Update examples to best practices
- Note version requirements

---

## Template: Converting .md to .mdx

### Input (.md file)
```markdown
# Workflow Triggers

Triggers start workflows when events happen.

## Types of Triggers

- Event triggers
- Schedule triggers
- Manual triggers

## Example

trigger: 'user.signup'
```

### Output (.mdx file)
```mdx
---
title: Workflow triggers
description: Learn how to use triggers to start workflows automatically when events occur in your application.
---

Triggers define when a workflow should start executing. You can configure workflows to run in response to events, on a schedule, or manually.

## Types of triggers

Workflow Builder supports three types of triggers:

- **Event triggers** - Start workflows when specific events occur (e.g., user signup, payment received)
- **Schedule triggers** - Run workflows at specified times or intervals
- **Manual triggers** - Start workflows on-demand via API or UI

## Configure an event trigger

Set up a trigger that starts a workflow when a user signs up:

```javascript
const workflow = {
  name: 'Welcome new users',
  trigger: {
    type: 'event',
    event: 'user.signup'
  },
  actions: [
    // Actions to perform
  ]
}
```

<Note>
Event triggers execute immediately when the event occurs. For delayed execution, use schedule triggers instead.
</Note>

## Next steps

- Learn about [workflow actions](/engine/workflow-builder/concepts/actions)
- See [trigger configuration reference](/engine/workflow-builder/reference/api#triggers)
- View [example workflows](/engine/workflow-builder/reference/examples)
```

---

## Execution Instructions for Another Agent

### Prerequisites
You need access to:
- All 15 .md files in engine/workflow-builder/
- Existing overview.mdx file
- docs.json navigation structure
- File system read/write capabilities

### Step-by-Step Execution

1. **Discovery Phase**
```
- List all files in engine/workflow-builder/
- Read each .md file and note its content
- Read existing overview.mdx
- Read current navigation structure
```

2. **Planning Phase**
```
- Categorize the 15 files by topic
- Determine which content updates existing docs
- Determine which content needs new files
- Plan navigation structure
- Create task list with all files to create/update
```

3. **Transformation Phase**
```
For each source .md file:
  - Extract main topic and subtopics
  - Determine target .mdx filename and path
  - Add YAML frontmatter with title and description
  - Convert markdown to MDX format
  - Add language tags to code blocks
  - Format headings to sentence case
  - Add callouts where appropriate
  - Add cross-references to related pages
  - Write the .mdx file
```

4. **Navigation Phase**
```
- Read current docs.json
- Update navigation structure with new pages
- Organize into logical groups
- Ensure proper hierarchy
- Write updated docs.json
```

5. **Verification Phase**
```
- Verify all files created successfully
- Check navigation structure is valid
- Ensure no broken links
- Confirm all frontmatter is present
- Validate MDX syntax
```

6. **Completion Phase**
```
- Provide summary of all files created/updated
- List navigation changes made
- Note any issues or decisions made
- Confirm documentation is complete
```

### Example Task List Format
```
1. Read all 15 .md files ✓
2. Analyze content and categorize ✓
3. Update overview.mdx ✓
4. Create quickstart.mdx ✓
5. Create concepts/workflows.mdx ✓
6. Create concepts/triggers.mdx ✓
... (continue for all files)
15. Update navigation in docs.json ✓
16. Verify all links work ✓
```

---

## Common Pitfalls to Avoid

1. **Don't create duplicate content** - Check existing docs first
2. **Don't skip frontmatter** - Every file needs title and description
3. **Don't use title case** - Use sentence case for headings
4. **Don't forget language tags** - All code blocks need them
5. **Don't break navigation** - Ensure paths match file locations
6. **Don't leave TODOs** - Complete all content fully
7. **Don't use marketing language** - Keep it technical and direct
8. **Don't skip examples** - Show working code
9. **Don't forget cross-references** - Link related content
10. **Don't ignore existing patterns** - Match the style of existing docs

---

## Success Criteria

Documentation is complete when:
- ✓ All 15 .md files are transformed to .mdx
- ✓ All files have proper frontmatter
- ✓ Navigation structure is updated and valid
- ✓ All code blocks have language tags
- ✓ All headings use sentence case
- ✓ Content follows Mintlify standards
- ✓ No broken links
- ✓ No duplicate content
- ✓ Logical organization and hierarchy
- ✓ Cross-references between related pages
- ✓ Examples are complete and practical
- ✓ User can navigate from overview to any topic
- ✓ Content is technically accurate
- ✓ Writing is clear and concise

---

## Contact and Support

If you encounter issues during documentation generation:
1. Review this plan thoroughly
2. Check existing documentation patterns
3. Verify file paths and navigation structure
4. Ensure all source files are accessible
5. Validate MDX syntax before writing files
