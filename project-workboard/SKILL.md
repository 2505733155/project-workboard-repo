---
name: project-workboard
description: Use when working on any long-term, non-one-off project, software or otherwise, or creating or maintaining its task board. Skip projects with a recorded user opt-out.
---

# Project Workboard

English (execution source) | [Chinese reading translation](SKILL.cn.md)

## Apply

Use the project instruction file recognized by the active AI tool (for example, `AGENTS.md` or `CLAUDE.md`), following existing project conventions.

If uncertain whether a project needs a workboard, ask the user. If declined, briefly record the opt-out in that project instruction file; do not create a board or invoke this skill for that project unless the user reverses the decision.

## Create

Reuse an existing project board in its current format. Updating this skill does not authorize migrating an existing board or its browser storage. When starting a project that needs a new board, or redesigning a board, list the HTML files in this skill's `assets/example/` directory and ask the user to choose an example before proceeding. Even if there is only one HTML file, ask the user to confirm it; if the user has already explicitly selected a file, use that selection without asking again. If no HTML files are available, ask the user to add one or provide an example before proceeding.

Users may replace the bundled [map example](assets/example/workboard-map.html) or add their own map HTML files alongside it in `assets/example/`. Discover the available map examples each time one is needed; do not require this particular filename.

Inspect the selected HTML and adapt its layout and interactions to the user's needs. Replace its project data, history, completion states and project-specific links. Create the project's board separately, preserving the example. The closing order below overrides the selected example.

When creating or redesigning a map, or changing its data structure or interactions, follow the [workboard format reference](references/workboard-format.md). New boards use a task map with right-side details. Keep one authoritative task source; replace the fictional content, current-task ID, project-root path and project-specific storage key.

Use explicit parent fields for hierarchy and separate dependency fields. Adding a business level or changing the established hierarchy requires user confirmation. Adding tasks within authorized scope and existing levels follows that authorization; expanding, collapsing and locating existing nodes are view operations.

Add a concise English instruction to the project instruction file, using the actual board path:

> Before project work, read `<board>.html` and update it after authorized work.

## Maintain

Read the board before work. After authorized work, update progress, next actions, statuses, evidence and history to reflect what actually happened.

For a task with, or planned to have, more than eight direct subtasks, propose display categories when planning the split or starting work on that parent, and obtain user approval before adding the category layer or changing its scheme. Maintain explicit groups and member lists under the approved scheme; do not automatically regroup by status. Record a declined proposal in the board and avoid repeating it without a meaningful change.

Use the following task-state semantics. Existing status names may be retained; make their mapping to these meanings explicit in the board.

| State | When to use |
| --- | --- |
| Todo / Not started | Planned but not currently being worked on, including downstream work, deferred tasks and inactive alternatives, even if prerequisites are missing. |
| In progress | Actively being worked on now, with a next step the agent can carry out autonomously. |
| Blocked / Needs user input | Scheduled to advance now, but unable to continue without information, a decision or an action from the user. Both conditions must hold. |
| Done | Work and required verification are complete, with supporting evidence. |

For each blocked item, state exactly what the user needs to do and the condition that will unblock it. Dependencies or technical difficulties alone do not make a task blocked: a failed test that the agent can keep diagnosing is in progress; work not scheduled to advance now remains todo. When work is deferred or no longer actively pursued, promptly move the task out of in progress to the appropriate state.

Preserve failure history, dependency relationships and unfinished work when changing status. These rules guide scheduling and user collaboration; they do not change acceptance criteria.

End every phase with four separate tasks in this fixed order:

1. **Independent verification and corrections.** Write requirements in the project root, identifying the phase/version, materials, checks and acceptance criteria. Give the user a prompt referencing that file and ask them to open a new conversation for verification. The implementing conversation, including its subagents, cannot fulfill this task. Record findings, corrections and re-verification before completion.
2. **User review.** Address the user's feedback and obtain their explicit confirmation that the review is complete.
3. **Experience consolidation and reuse (optional).** Ask once whether to summarize the phase's user instructions, review feedback and useful practices identified by the agent for future reuse. If declined, record that this task was skipped for this phase and proceed to cleanup without asking again. If accepted, follow [experience reuse guidance](references/experience-reuse.md) to let the user select lessons, confirm their scope and choose how to preserve them. Record the outcome and any saved locations in the board.
4. **Full work-directory inspection and cleanup.** Inspect the working directory and remove confirmed temporary or redundant artifacts, preserving deliverables, necessary evidence and user changes.

Keep this skill minimal; extend it using actual usage feedback.
