# Persona Builder

Build the final Persona markdown file from the analysis.

## Instructions

Take the extracted persona from the analysis phase and build a clean, five-layer structured markdown file.

**Structure must be exactly this:**

```markdown
# Persona: {Role Name}

## Layer 0: Hard Rules
- Rule 1 (highest priority, always follows)
- Rule 2
- ...

## Layer 1: Basic Identity
- Role: ...
- Field: ...
- {Any other basic info}

## Layer 2: Communication Style
- ...
- ...

## Layer 3: Decision Pattern
- ...
- ...

## Layer 4: Interaction Pattern
- ...
- ...

## Correction Log
{Leave this section empty for now, it will be filled with corrections later.}
```

## Guidelines

- **Must** keep the five-layer structure exactly as above
- Each point should be a **concrete behavior**, not just an adjective
- Instead of "strict", write "Points out mistakes clearly and directly, doesn't beat around the bush"
- Instead of "talkative", write "Gives detailed explanations, often asks follow-up questions to keep the conversation going"
- Be specific about behavior, not just traits
- If no information provided for a layer, just leave it with "No specific information provided."
- The AI will use this every time it responds, so every rule should be actionable
