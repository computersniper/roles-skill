# Incremental Merger

## Instructions

User provided new materials for an existing role. Analyze the new content and merge it into the existing knowledge/persona.

### Steps:

1. **Identify what's new**: What new information does this add that wasn't there before?
2. **Check for conflicts**: Does this contradict anything in the existing version?
3. **Propose merge**: Should it be appended, or should some part be replaced?
4. **Output the full updated content**: Give the complete new version of the file(s).

### Merge Principles

- **Prefer keep existing**: Don't remove existing content unless the new information clearly contradicts it
- **Append incremental**: Add new information at the end of the appropriate section
- **Version control**: The old version is already archived by the version manager, so it's safe to update
- **Update meta**: Remember to increment the version number in meta.json and update updated_at timestamp

### Conflict Resolution

If there's a conflict:
- If it's a clear correction (user says "this is wrong"), replace the conflicting section
- If it's additional information, keep both and note the addition
- If it's a difference of opinion, keep both and note the difference
