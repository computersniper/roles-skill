# Knowledge Analyzer

## Goal

Analyze the provided source materials (text, documents, notes) and extract the **Role Knowledge** that this role should have.

## Extraction Dimensions

Extract information along these dimensions:

### 1. Domain & Scope
- What professional field does this role belong to?
- What problems does this role solve?
- What are the main areas of expertise?
- What topics are within scope vs out of scope?

### 2. Core Capabilities
- What can this role do?
- What services does this role provide?
- What problems is this role especially good at solving?

### 3. Methodology & Process
- What methodology does this role follow?
- What's the typical process when solving a problem?
- Are there any step-by-step frameworks?

### 4. Principles & Rules
- What are the core principles this role adheres to?
- What are the hard rules that must never be broken?
- What are the common pitfalls this role avoids?

### 5. Knowledge Structure
- What are the key concepts this role uses?
- What's the typical knowledge organization?
- Are there any common frameworks or models?

### 6. Style of Problem Solving
- Does this role prefer simplicity or complexity?
- Does this role emphasize theory first or practice first?
- What's the approach to explaining things?

## Adapt to Role Type

Adjust extraction based on the role type:

- **Teacher/Tutor**: Focus on teaching methods, explanation style, what topics they teach, how they answer questions
- **Artist/Musician**: Focus on style, genre, creative philosophy, what kind of works they create
- **Therapist/Counselor**: Focus on listening approach, therapeutic orientation, how they interact
- **Coach/Trainer**: Focus on methodology, assessment, goal-setting, feedback style
- **Chef**: Focus on cuisine, ingredients, cooking methods, flavor preferences

## Output Format

Organize your extraction in clear sections with bullet points. Keep it concise but comprehensive. Don't repeat yourself.

```
## Domain: {domain}
- ...

## Core Capabilities:
- ...

## Methodology:
- ...

## Principles:
- ...
```

## Incremental Analysis

If this is an incremental update (merging new materials into existing knowledge):
1. Identify what new information this adds
2. Note any conflicts with existing knowledge
3. Suggest how to merge (replace vs append)
