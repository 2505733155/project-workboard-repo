# Project Workboard · 项目任务看板

简体中文 | [English](README.en.md)

一个面向长期项目的轻量 AI skill：让 AI 在工作前读取项目看板，在完成授权工作后更新进展，把任务、下一步行动、证据和历史记录留在项目自己的 HTML 文件中。

适合论文返修、科研实验、软件开发等需要多轮推进的项目。技能规则见 [SKILL.md](SKILL.md)。

技能由 Markdown 指令和 HTML 案例组成，可用于能够加载 `SKILL.md`、访问配套资源并读写项目文件的 AI 工具，例如 Codex、Claude Code、WorkBuddy。安装路径、调用入口和项目指令文件随工具及其配置而变化。

## 它会做什么

- 优先复用项目已有的看板；需要新建或重新设计时，由用户选择 HTML 案例。
- 根据项目目标调整案例的布局和交互，替换任务、历史、完成状态及项目链接。
- 在当前 AI 工具识别的项目指令文件（如 `AGENTS.md`、`CLAUDE.md`）中记录看板路径，指导后续工作先读看板、完成授权工作后再更新。
- 维护实际进展、下一步行动、任务状态、证据和历史记录。
- 为每个阶段依次安排独立核验与修正、用户审阅、工作目录检查与清理。

这是由 AI 执行的文件维护流程。项目看板由 AI 更新 HTML 后，在浏览器中刷新查看；它不自动扫描项目并同步进度。

## 安装

需要能够加载本技能并读取和编辑项目文件的 AI 工具，以及用于查看 HTML 的现代浏览器。此 skill 无需额外安装 Python、Node.js、服务器或包管理器。

1. 在本仓库的 GitHub 页面选择 **Code → Download ZIP**，下载并解压。
2. 保留包含 `SKILL.md` 和 `assets/` 的完整技能目录，按所用工具的方式安装到技能目录，或通过技能面板导入。
3. 在该工具的技能列表或调用入口中选择 `project-workboard`。如果没有识别到新技能，按该工具的要求刷新或重新启动会话。

| 工具或安装配置 | 用户级目录示例（当前用户的所有项目） | 项目级目录示例（仅当前项目） |
| --- | --- | --- |
| Codex（已有 `.codex` 安装） | `~/.codex/skills/project-workboard/` | 沿用当前配置中的项目技能目录 |
| Codex（当前官方文档） | `~/.agents/skills/project-workboard/` | `<项目根目录>/.agents/skills/project-workboard/` |
| Claude Code | `~/.claude/skills/project-workboard/` | `<项目根目录>/.claude/skills/project-workboard/` |

`~` 表示用户主目录；Windows 中通常对应 `C:\Users\你的用户名`。例如，使用 `.codex` 目录的 Windows 安装可放在 `C:\Users\你的用户名\.codex\skills\project-workboard\`。路径由工具、版本及安装配置决定，沿用当前能够识别技能的目录即可，无需仅为此 skill 迁移或在多个目录重复安装。目录规则见 [Codex 官方文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)和 [Claude Code 官方文档](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

WorkBuddy 可在技能板块选择 **添加技能 → 上传技能**，导入包含 `SKILL.md` 和 `assets/` 的本地技能包；具体包格式与导入要求以所用版本为准，参阅 [WorkBuddy 官方技能文档](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。其他 AI 工具也按各自的技能目录或导入方式安装。

请保留以下目录关系，不能只复制 `SKILL.md`：

```text
project-workboard/
├── SKILL.md
└── assets/
    └── example/
        └── AMPC_ISA_revision_board.html
```

如果已有安装，更新前保留自己添加或替换的 HTML 案例。README 和许可证可随目录一起保留。

## 开始使用

以下仅以 Codex 为例展示调用方式；其他 AI 工具使用各自的技能调用入口，工作流程相同。在目标项目目录中打开 Codex，并说明项目目标：

```text
$project-workboard 为我的论文返修项目建立任务看板。
先了解审稿意见和现有材料，再让我选择 HTML 案例；将看板保存为项目根目录的 revision_board.html。
```

已有看板时，可以直接指定：

```text
$project-workboard 先读取项目根目录的 revision_board.html，
继续处理当前任务，并在完成授权工作后更新进展、证据和下一步行动。
```

看板生成后，用浏览器打开项目中的 HTML 文件查看。内置案例提供主题导航、状态筛选、任务搜索、历史记录和临时草稿；新看板的具体交互取决于所选案例及项目需求。内置案例的临时草稿保存在当前浏览器中，也可下载为文本，不会自动写回 HTML 或在设备之间同步。

## 选择或添加自己的 HTML 案例

案例目录为此 skill 内的 [`assets/example/`](assets/example/)。你可以替换内置案例，也可以把自己的 HTML 文件放到该目录，与现有案例并存；无需沿用内置文件名。

- **多个 HTML**：AI 列出可用文件，请用户选择。
- **只有一个 HTML**：AI 仍需请用户确认。
- **用户已明确指定文件**：直接使用该选择，不重复询问。
- **目录中没有 HTML**：AI 请用户添加或提供案例后再继续。
- **项目已有看板**：优先继续维护，无需每次工作都重新选择案例。

内置的 [AMPC_ISA_revision_board.html](assets/example/AMPC_ISA_revision_board.html) 是论文返修看板案例，界面以中文为主，包含原项目的任务、历史及材料链接。相关项目材料不随本仓库提供。创建新看板时，AI 会替换这些项目内容和链接，将结果保存在目标项目中，保留案例文件供后续使用。

## 阶段如何收尾

每个阶段按以下顺序安排三个独立任务，以 [SKILL.md](SKILL.md) 的规则为准：

1. **独立核验与修正**：在项目根目录写出核验要求，给出引用该文件的提示词，请用户另开新对话核验；记录发现、修正和再次核验。当前实施对话及其子代理不能代替独立核验。
2. **用户审阅**：处理反馈，并取得用户对本轮审阅结束的明确确认。
3. **工作目录检查与清理**：检查工作目录，移除确认无用的临时或重复产物，保留交付物、必要证据和用户改动。

如果不希望某个项目使用看板，可以明确告知当前 AI 助手。技能会在该工具识别的项目指令文件中简短记录退出选择；用户重新启用前，不为该项目创建看板或调用本技能。

## 仓库结构

```text
project-workboard/
├── SKILL.md                 # AI 读取的技能规则
├── README.md                # 中文说明（默认首页）
├── README.en.md             # 英文说明
├── LICENSE                  # MIT 许可证
├── .gitignore               # 系统及编辑器临时文件忽略规则
└── assets/
    └── example/             # 可替换、可并存的 HTML 案例
        └── AMPC_ISA_revision_board.html
```

## 许可证

本项目采用 [MIT License](LICENSE)。
