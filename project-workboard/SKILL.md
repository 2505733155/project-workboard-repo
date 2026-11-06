---
name: project-workboard
description: Use when working on any long-term, non-one-off project, software or otherwise, or creating or maintaining its task board. Skip projects with a recorded user opt-out.
---

# Project Workboard

## Apply

Use the project instruction file recognized by the active AI tool (for example, `AGENTS.md` or `CLAUDE.md`), following existing project conventions.

If uncertain whether a project needs a workboard, ask the user. If declined, briefly record the opt-out in that project instruction file; do not create a board or invoke this skill for that project unless the user reverses the decision.

## Create

Reuse an existing project board. When starting a project that needs a new board, or redesigning a board, list the HTML files in this skill's `assets/example/` directory and ask the user to choose an example before proceeding. Even if there is only one HTML file, ask the user to confirm it; if the user has already explicitly selected a file, use that selection without asking again. If no HTML files are available, ask the user to add one or provide an example before proceeding.

Users may replace the bundled [example](assets/example/AMPC_ISA_revision_board.html) with their own HTML, or add other HTML files alongside it in `assets/example/`. Discover the available files each time an example is needed; do not require this particular filename.

Inspect the selected HTML and adapt its layout and interactions to the user's needs. Replace its project data, history, completion states and project-specific links. Create the project's board separately, preserving the example. The closing order below overrides the selected example.

Add a concise English instruction to the project instruction file, using the actual board path:

> Before project work, read `<board>.html` and update it after authorized work.

## Maintain

Read the board before work. After authorized work, update progress, next actions, statuses, evidence and history to reflect what actually happened.

End every phase with three separate tasks in this fixed order:

1. **Independent verification and corrections.** Write requirements in the project root, identifying the phase/version, materials, checks and acceptance criteria. Give the user a prompt referencing that file and ask them to open a new conversation for verification. The implementing conversation, including its subagents, cannot fulfill this task. Record findings, corrections and re-verification before completion.
2. **User review.** Address the user's feedback and obtain their explicit confirmation that the review is complete.
3. **Full work-directory inspection and cleanup.** Inspect the working directory and remove confirmed temporary or redundant artifacts, preserving deliverables, necessary evidence and user changes.

Keep this skill minimal; extend it using actual usage feedback.
