# Project Workboard · 项目任务看板

简体中文 | [English](README.en.md)

一个面向长期项目的轻量 AI skill：让 AI 在工作前读取项目看板，在完成授权工作后更新进展，把任务、下一步行动、证据和历史记录留在项目自己的 HTML 文件中。

适合论文返修、科研实验、软件开发等需要多轮推进的项目。技能规则见 [SKILL.md](project-workboard/SKILL.md)。

技能由 Markdown 指令、参考文档和 HTML 案例组成，可用于能够加载 `SKILL.md`、访问配套资源并读写项目文件的 AI 工具，例如 Codex、Claude Code、WorkBuddy。安装路径、调用入口和项目指令文件随工具及其配置而变化。

## 为什么使用工作面板

- **让进度看得见**：面板是人与 AI 智能体交互的共同窗口，将目标、计划、当前任务、完成证据和待决事项集中展示，便于人随时了解工作进展并调整方向。
- **减少逐步监督的负担**：在面板中明确目标、制定计划并约定验收标准后，AI 智能体可以在授权范围内连续推进任务。人主要在方案确认、阶段验收和需要决策等关键节点检查工作、进行必要调整，把精力集中在判断与决策上。

## 它会做什么

- 优先复用项目已有的看板；需要新建或重新设计时，由用户选择 HTML 案例。
- 根据项目目标调整案例的布局和交互，替换任务、历史、完成状态及项目链接。
- 在当前 AI 工具识别的项目指令文件（如 `AGENTS.md`、`CLAUDE.md`）中记录看板路径，指导后续工作先读看板、完成授权工作后再更新。
- 维护实际进展、下一步行动、任务状态、证据和历史记录。
- 为每个阶段依次安排独立核验与修正、用户审阅、可选的经验总结与复用、工作目录检查与清理。

这是由 AI 执行的文件维护流程。项目看板由 AI 更新 HTML 后，在浏览器中刷新查看；它不自动扫描项目并同步进度。

## 安装

需要能够加载本技能并读取和编辑项目文件的 AI 工具，以及用于查看 HTML 的现代浏览器。此 skill 无需额外安装 Python、Node.js、服务器或包管理器。

### 通过智能体安装

如果你使用的智能体支持访问网络和管理本地技能，可以直接发送以下提示词：

```text
https://github.com/2505733155/project-workboard-repo
请你将仓库内的 project-workboard/ skill（包含 SKILL.md、references/ 和 assets/）安装到当前智能体使用的用户级技能目录，供我的各个项目使用。
安装后请确认文件完整，并告诉我实际安装路径和如何启用。如果已有安装，请保留我自定义的案例和修改。
```

### 手动安装

1. 在本仓库的 GitHub 页面选择 **Code → Download ZIP**，下载并解压。
2. 找到解压后仓库根目录中的 `project-workboard/` 子目录；将这个包含 `SKILL.md`、`references/` 和 `assets/` 的完整子目录安装到所用工具的技能目录，或按该工具的要求打包后通过技能面板导入。
3. 在该工具的技能列表或调用入口中选择 `project-workboard`。如果没有识别到新技能，按该工具的要求刷新或重新启动会话。

| 工具或安装配置 | 用户级目录示例（当前用户的所有项目） | 项目级目录示例（仅当前项目） |
| --- | --- | --- |
| Codex（已有 `.codex` 安装） | `~/.codex/skills/project-workboard/` | 沿用当前配置中的项目技能目录 |
| Codex（当前官方文档） | `~/.agents/skills/project-workboard/` | `<项目根目录>/.agents/skills/project-workboard/` |
| Claude Code | `~/.claude/skills/project-workboard/` | `<项目根目录>/.claude/skills/project-workboard/` |

`~` 表示用户主目录；Windows 中通常对应 `C:\Users\你的用户名`。例如，使用 `.codex` 目录的 Windows 安装可放在 `C:\Users\你的用户名\.codex\skills\project-workboard\`。路径由工具、版本及安装配置决定，沿用当前能够识别技能的目录即可，无需仅为此 skill 迁移或在多个目录重复安装。目录规则见 [Codex 官方文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)和 [Claude Code 官方文档](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

WorkBuddy 可在技能板块选择 **添加技能 → 上传技能**，导入包含 `SKILL.md`、`references/` 和 `assets/` 的本地技能包；具体包格式与导入要求以所用版本为准，参阅 [WorkBuddy 官方技能文档](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。其他 AI 工具也按各自的技能目录或导入方式安装。

请保留以下目录关系，不能只复制 `SKILL.md`：

```text
project-workboard/
├── SKILL.md
├── references/
│   └── experience-reuse.md
└── assets/
    └── example/
        ├── AMPC_ISA_revision_board.html
        └── chap02_requirements_board.html
```

如果已有安装，更新前保留自己添加或替换的 HTML 案例。仓库根目录的 README 和许可证也可一并复制到安装后的技能目录中。

希望通过 Git 安装并持续获取更新，可阅读 [Git 与 GitHub 新手指南](docs/git-guide.md)。指南以 VS Code 和 GitHub 网页操作为主，附有命令行步骤，并说明如何将仓库更新同步到已安装的技能目录。

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

看板生成后，用浏览器打开项目中的 HTML 文件查看。内置案例提供导航、状态筛选、任务搜索、历史记录和临时草稿；新看板的具体交互取决于所选案例及项目需求。内置案例的临时草稿保存在当前浏览器中，也可下载为文本，不会自动写回 HTML 或在设备之间同步。

## 选择或添加自己的 HTML 案例

案例目录为此 skill 内的 [`assets/example/`](project-workboard/assets/example/)，在本仓库中的路径为 `project-workboard/assets/example/`。你可以替换内置案例，也可以把自己的 HTML 文件放到该目录，与现有案例并存；无需沿用内置文件名。

- **多个 HTML**：AI 列出可用文件，请用户选择。
- **只有一个 HTML**：AI 仍需请用户确认。
- **用户已明确指定文件**：直接使用该选择，不重复询问。
- **目录中没有 HTML**：AI 请用户添加或提供案例后再继续。
- **项目已有看板**：优先继续维护，无需每次工作都重新选择案例。

内置两个案例，可按工作规模选择：

| 案例 | 适用工作 | 阶段选项卡 |
| --- | --- | --- |
| [AMPC_ISA_revision_board.html](project-workboard/assets/example/AMPC_ISA_revision_board.html) | 较大型、需要分阶段推进的工作，例如整篇毕业论文的修改 | 有，可切换不同阶段 |
| [chap02_requirements_board.html](project-workboard/assets/example/chap02_requirements_board.html) | 较小型、范围集中的工作，例如毕业论文中某一章的修改 | 无，在同一页面集中查看任务 |

两个案例均以中文为主，包含原项目的任务、历史及材料链接。相关项目材料不随本仓库提供。创建新看板时，AI 会替换这些项目内容和链接，将结果保存在目标项目中，保留案例文件供后续使用。

## 阶段如何收尾

每个阶段按以下顺序安排四个独立任务，以 [SKILL.md](project-workboard/SKILL.md) 的规则为准：

1. **独立核验与修正**：在项目根目录写出核验要求，给出引用该文件的提示词，请用户另开新对话核验；记录发现、修正和再次核验。当前实施对话及其子代理不能代替独立核验。
2. **用户审阅**：处理反馈，并取得用户对本轮审阅结束的明确确认。
3. **经验总结与复用（可选）**：先提醒用户是否总结本阶段的指示、审阅建议和智能体发现的有效做法。不同意则记录本阶段已跳过，直接继续清理；同意后，由用户筛选候选经验、确定项目级或用户级范围，并选择保存方式。优先维护已有文档或技能，项目指令文件保持简短，通过链接按需引用详细经验；结果及保存位置记入看板。具体原则见[经验复用参考](project-workboard/references/experience-reuse.md)。
4. **工作目录检查与清理**：检查工作目录，移除确认无用的临时或重复产物，保留交付物、必要证据和用户改动。

如果不希望某个项目使用看板，可以明确告知当前 AI 助手。技能会在该工具识别的项目指令文件中简短记录退出选择；用户重新启用前，不为该项目创建看板或调用本技能。

## 反馈与参与改进

- 遇到问题或有功能建议，可以在 [Issues](https://github.com/2505733155/project-workboard-repo/issues) 提交反馈。
- 希望改进说明、技能规则或添加 HTML 案例，可以 Fork 仓库，在自己的分支中修改后提交 Pull Request。
- 初次使用 Git 或 GitHub，请从 [新手指南](docs/git-guide.md) 开始，了解安装、更新、Issue、Fork、分支、提交和 Pull Request 的完整流程。

## 仓库结构

```text
project-workboard-repo/
├── README.md                # 中文说明（默认首页）
├── README.en.md             # 英文说明
├── LICENSE                  # MIT 许可证
├── .gitignore               # 系统及编辑器临时文件忽略规则
├── docs/                    # Git 新手指南及项目文档
│   ├── git-guide.md         # 中文指南
│   └── git-guide.en.md      # 英文指南
└── project-workboard/       # 可直接安装的技能目录
    ├── SKILL.md             # AI 读取的技能规则
    ├── references/          # 用户同意总结经验后按需读取
    │   └── experience-reuse.md
    └── assets/
        └── example/         # 可替换、可并存的 HTML 案例
            ├── AMPC_ISA_revision_board.html
            └── chap02_requirements_board.html
```

## 致谢

感谢清华大学航空发动机研究院博士生刘晟奕同学，最早提出使用这一方法和思路，为本项目的形成提供了启发。

## 许可证

本项目采用 [MIT License](LICENSE)。
