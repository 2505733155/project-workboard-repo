# Experience Consolidation and Reuse

Read this guide after the user agrees to the optional experience-reuse task, between user review and work-directory cleanup.

## Select lessons with the user

Review the phase's user instructions and review feedback, and propose useful practices the agent observed. Present concise candidates with their context and where they may help again. Agent observations are suggestions for the user to select, not automatically accepted rules.

Separate one-off task choices from lasting lessons. Confirm which selected lessons apply only to this project and which represent user preferences or workflows suitable for other projects. Agreement to summarize does not by itself make every candidate a user-wide rule. If no candidates are worth keeping, record that outcome and continue without creating files.

## Choose a form that fits

Follow the user's preferred form and location when available. If the user has already selected the content, scope or destination, use those choices rather than asking again. Otherwise, recommend the simplest suitable option and explain its tradeoff; discuss other forms only when they would meet a concrete need.

| Content and intended use | Suitable form | Tradeoff |
| --- | --- | --- |
| Project terminology, review expectations or recurring project conventions | Update existing topic documents; create a focused document under `docs/` when needed | Explicit and easy to maintain with the project; future agents need a discoverable reading entry point |
| User-wide preferences that should apply across projects | The active tool's user-level instructions or an existing user-maintained reference | Reusable across projects; scope must be confirmed so project-specific choices stay local |
| A repeatable workflow or technique | Update a relevant existing skill; propose a new skill only for an independently useful, lasting workflow | Can bundle instructions and resources; adds something to discover and maintain |
| Useful context for future recall, when the tool supports it | The tool's native memory capability | Depends on the tool's controls, availability and recall behavior; important required rules still need explicit guidance |
| A need already met by a third-party learning tool | An available community skill or tool chosen with the user | May add logging, automation or dependencies; inspect the specific source and actual behavior before recommending it |

When choosing a skill, use an available skill-authoring tool such as `skill-creator`, or the active tool's equivalent workflow. Prefer extending an existing relevant skill to creating a duplicate. A short project convention usually belongs in a project document rather than a new skill.

Memory services and community skills are optional choices, not prerequisites for completing this task. For Codex memories, consult the [official memory documentation](https://learn.chatgpt.com/docs/customization/memories) and current controls: memory generation runs in the background and may not happen immediately. Do not use manual edits to generated memory files as the default workflow or keep the phase open waiting for a background memory update. Report what was actually configured or prepared rather than claiming unverified storage.

For a community option, identify its exact repository or package, inspect its instructions, and explain the relevant compatibility, storage, automation and maintenance requirements. A name alone is not enough to compare tools. Discuss installing a new dependency or changing user-level settings as part of the chosen method, rather than treating consent to summarize as consent to those changes.

## Keep instruction files short

Keep detailed lessons in focused documents, reusing existing files where possible. Separate topics such as terminology and review expectations when they serve different activities. Add only a short purpose and conditional reading link to the project instruction file recognized by the active tool, such as `AGENTS.md` or `CLAUDE.md`.

For example, the instruction file can contain:

```text
When writing or revising the manuscript, follow docs/terminology.md.
Before a phase review, read docs/review-guidelines.md.
```

Use the project's real file paths and relevant reading conditions. Do not turn the entry point into the full experience archive or require every lesson document to be read before every task. Apply the same principle to user-level guidance when detailed supporting references are needed.

## Preserve the agreed result

Once the user has selected the lessons, scope and form, make the agreed changes and check their links or other relevant behavior. Record the decision, scope and saved locations in the board; distinguish an adopted lesson from a proposed one and an executed change from a pending action.

If the user declines the optional task, record the skip for this phase and continue to cleanup without repeating the question. A phase-level skip does not opt the project out of workboard use. Use the board's existing status conventions, noting the skip in the task description or history when its status list has no dedicated skipped state.
