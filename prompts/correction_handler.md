# Correction Handler

## User says: "X wouldn't do it that way, X would do it this way instead..."

Your job: extract the correction and add it to the appropriate file.

### Steps:

1. **Identify the type**: Is this correcting the **Knowledge** (professional knowledge/method) or the **Persona** (personality/style)?
2. **Extract the correction**: What exactly is the correction? What should it be instead?
3. **Add to Correction Log**: Append a new entry at the end of the `## Correction Log` section:
   ```
   ### {date}: Correction
   {User's correction in their own words}

   **Applied change**: {what we changed}
   ```
4. **Update the relevant section**: Apply the correction to the appropriate place in the document
5. **Regenerate the full SKILL.md**: Combine the updated knowledge and persona into the full skill
6. **Update meta**: Increment corrections count, update version, update updated_at timestamp

### Guidelines

- Keep the user's original wording in the Correction Log for future reference
- Don't delete the old content, just append the correction
- The Correction Log is for auditing, it doesn't affect runtime behavior (the change is already applied to the main content)
- One correction usually changes one or two points, don't rewrite the whole file unless necessary
