# Project Workboard

[简体中文](README.md) | English

A lightweight AI skill for long-term projects. It guides the AI to read a project board before working and update it after authorized work, keeping tasks, next actions, evidence, and history in the project's own HTML file.

Use it for paper revisions, research experiments, software development, and other projects spanning multiple work sessions. The skill's instructions are in [SKILL.md](project-workboard/SKILL.md).

The skill consists of Markdown instructions and HTML examples. It can be used with AI tools that load `SKILL.md`, access supporting resources, and read and edit project files, such as Codex, Claude Code, and WorkBuddy. Installation paths, invocation methods, and project instruction files depend on the tool and its configuration.

## Why use a workboard

- **Make progress visible:** the board gives people and AI agents a shared window into goals, plans, current tasks, completion evidence, and open decisions. It helps people monitor progress and adjust direction.
- **Reduce step-by-step supervision:** once goals, plans, and acceptance criteria are agreed on, the AI agent can work through tasks within the authorized scope. People can focus their reviews and adjustments on key points such as approving a plan, reviewing a phase, or making a decision.

## What it does

- Reuses an existing project board; asks the user to choose an HTML example when creating or redesigning a board.
- Adapts the example's layout and interactions, replacing its tasks, history, completion states, and project links.
- Records the board path in a project instruction file recognized by the active AI tool, such as `AGENTS.md` or `CLAUDE.md`, so subsequent work starts by reading the board and ends by updating it after authorized work.
- Maintains actual progress, next actions, task statuses, evidence, and history.
- Ends each phase with independent verification and corrections, user review, and work-directory inspection and cleanup, in that order.

This is a file-maintenance workflow carried out by the AI. Refresh the board in your browser after the AI updates its HTML; the board does not scan the project or synchronize progress automatically.

## Installation

You need an AI tool that can load the skill and read and edit project files, and a modern browser to view the HTML. The skill requires no additional Python, Node.js, server, or package manager installation.

### Install with an AI agent

If your AI agent can access the network and manage local skills, send it this prompt:

```text
https://github.com/2505733155/project-workboard-repo
Please install the project-workboard/ skill from this repository, including SKILL.md and assets/, in the user-level skill directory recognized by the current AI tool, so I can use it across my projects.
Verify that the installed files are complete, and tell me the actual installation path and how to enable the skill. If an installation already exists, preserve my custom examples and edits.
```

### Install manually

1. On this repository's GitHub page, select **Code → Download ZIP** and extract the archive.
2. Find the `project-workboard/` subdirectory in the extracted repository root. Install this complete subdirectory, including `SKILL.md` and `assets/`, in your tool's skill directory, or package it as required by your tool and import it through the skills panel.
3. Select `project-workboard` through that tool's skill list or invocation interface. If it does not appear, refresh or restart the session as required by the tool.

| Tool or installation configuration | User-level directory example (all your projects) | Project-level directory example (current project only) |
| --- | --- | --- |
| Codex (existing `.codex` installation) | `~/.codex/skills/project-workboard/` | Use your configured project skill directory |
| Codex (current official documentation) | `~/.agents/skills/project-workboard/` | `<project-root>/.agents/skills/project-workboard/` |
| Claude Code | `~/.claude/skills/project-workboard/` | `<project-root>/.claude/skills/project-workboard/` |

`~` means your home directory, typically `C:\Users\your-username` on Windows. For example, a Windows installation using `.codex` can place the skill at `C:\Users\your-username\.codex\skills\project-workboard\`. Paths depend on the tool, version, and installation configuration. Use the directory your tool already recognizes; there is no need to migrate or install duplicate copies just for this skill. See the [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code documentation](https://code.claude.com/docs/en/skills#choose-where-skills-load) for directory conventions.

In WorkBuddy, use **Add skill → Upload skill** in the skills panel to import a local skill package containing `SKILL.md` and `assets/`. Follow your version's package-format and import requirements; see the [official WorkBuddy skills documentation](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market). Other AI tools use their own skill directories or import interfaces.

Preserve this directory structure; copying only `SKILL.md` is insufficient:

```text
project-workboard/
├── SKILL.md
└── assets/
    └── example/
        ├── AMPC_ISA_revision_board.html
        └── chap02_requirements_board.html
```

Before updating an existing installation, preserve any HTML examples you have added or replaced. You may also copy the README files and license from the repository root into the installed skill directory.

To install with Git and keep receiving updates, see the [Git and GitHub beginner's guide](docs/git-guide.en.md). It focuses on VS Code and the GitHub website, includes command-line steps, and explains how to copy repository updates into an installed skill directory.

## Getting started

The following examples use Codex only to illustrate invocation. Other AI tools use their own skill interfaces and follow the same workflow. Open Codex in the target project directory and describe your goal:

```text
$project-workboard Create a task board for my paper revision project.
Read the reviewer comments and existing materials, then ask me to choose an HTML example.
Save the board as revision_board.html in the project root.
```

For an existing board, specify it directly:

```text
$project-workboard Read revision_board.html in the project root,
continue the current task, and update progress, evidence, and next actions after authorized work.
```

Open the generated project HTML in a browser. The bundled examples include navigation, status filters, task search, history, and a scratchpad; a new board's interactions depend on the selected example and project needs. The bundled scratchpads save notes in the current browser and offer a text download. They do not write notes back to the HTML or synchronize them across devices.

## Choosing or adding HTML examples

Examples live in this skill's [`assets/example/`](project-workboard/assets/example/) directory, at `project-workboard/assets/example/` in this repository. Replace the bundled example or add your own HTML files alongside it. You do not need to keep the bundled filename.

- **Multiple HTML files:** the AI lists the available files and asks the user to choose.
- **One HTML file:** the AI still asks the user to confirm it.
- **A file already explicitly selected by the user:** the AI uses that selection without asking again.
- **No HTML files:** the AI asks the user to add or provide an example before proceeding.
- **An existing project board:** the AI prioritizes maintaining it, without requiring a new example selection for every work session.

Choose between the two bundled examples based on the scope of your work:

| Example | Suitable work | Phase tabs |
| --- | --- | --- |
| [AMPC_ISA_revision_board.html](project-workboard/assets/example/AMPC_ISA_revision_board.html) | Larger projects with multiple phases, such as revising an entire thesis | Yes, to switch between phases |
| [chap02_requirements_board.html](project-workboard/assets/example/chap02_requirements_board.html) | Smaller, focused projects, such as revising a single thesis chapter | No; tasks are presented together on one page |

Both examples have primarily Chinese interfaces and contain tasks, history, and material links from their original projects; those project materials are not included in this repository. When creating a new board, the AI replaces that project content and its links, saves the result in the target project, and preserves the example for future use.

## Closing a phase

Each phase ends with three separate tasks in this order, following [SKILL.md](project-workboard/SKILL.md):

1. **Independent verification and corrections:** write verification requirements in the project root, provide a prompt referencing that file, and ask the user to open a new conversation for verification. Record findings, corrections, and re-verification. The implementing conversation and its subagents cannot fulfill this independent verification task.
2. **User review:** address feedback and obtain the user's explicit confirmation that the review is complete.
3. **Work-directory inspection and cleanup:** inspect the working directory and remove confirmed temporary or redundant artifacts, preserving deliverables, necessary evidence, and user changes.

To opt a project out of workboard use, tell your current AI assistant explicitly. The skill records the opt-out briefly in a project instruction file recognized by that tool and will not create a board or run for the project until the user reverses that decision.

## Feedback and contributions

- Report problems or suggest improvements through [Issues](https://github.com/2505733155/project-workboard-repo/issues).
- To improve the documentation or skill instructions, or add an HTML example, fork the repository, make changes on your own branch, and submit a pull request.
- If you are new to Git or GitHub, start with the [beginner's guide](docs/git-guide.en.md) for installation, updates, issues, forks, branches, commits, and pull requests.

## Repository layout

```text
project-workboard-repo/
├── README.md                # Chinese documentation and default landing page
├── README.en.md             # English documentation
├── LICENSE                  # MIT license
├── .gitignore               # OS and editor temporary-file ignore rules
├── docs/                    # Git beginner's guides and project documentation
│   ├── git-guide.md         # Chinese guide
│   └── git-guide.en.md      # English guide
└── project-workboard/       # Installable skill directory
    ├── SKILL.md             # Instructions read by the AI
    └── assets/
        └── example/         # Replaceable HTML examples that can coexist
            ├── AMPC_ISA_revision_board.html
            └── chap02_requirements_board.html
```

## Acknowledgments

We thank 刘晟奕, a doctoral student at the Institute for Aero Engine, Tsinghua University, for first proposing this method and approach, which inspired this project.

## License

This project is licensed under the [MIT License](LICENSE).
