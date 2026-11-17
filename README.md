# Project Workboard · 项目任务导图

简体中文 | [English](README.en.md)

一个面向长期项目的轻量 AI skill：让 AI 在工作前读取项目看板，在完成授权工作后更新进展，把任务、下一步行动、证据和历史记录留在项目自己的 HTML 文件中。

适合论文返修、科研实验、软件开发等需要多轮推进的项目。技能执行规则见 [SKILL.md](project-workboard/SKILL.md)；供人阅读的中文译本包括[技能规则](project-workboard/SKILL.cn.md)和[经验复用指引](project-workboard/references/experience-reuse.cn.md)，规则以英文原文为准。

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
├── SKILL.cn.md
├── references/
│   ├── experience-reuse.md
│   ├── experience-reuse.cn.md
│   ├── workboard-format.md
│   └── workboard-format.cn.md
└── assets/
    └── example/
        └── workboard-map.html
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

看板生成后，用浏览器直接打开项目中的 HTML 文件。新版采用导图＋右侧详情，支持逐层展开、搜索编号或标题、定位当前任务、平移和缩放。展开节点即展示全部直属子任务；归属与依赖分别记录，阶段签收不由子项状态自动推断。

普通滚轮上下移动，Ctrl＋滚轮以指针位置缩放，Shift＋滚轮左右移动，左键或右键拖动背景平移；画布背景不弹出浏览器右键菜单。右侧详情独立滚动，窄屏可打开或收起右侧详情。临时草稿可在当前浏览器中保存或下载，不会自动发给智能体或写回 HTML；草稿和视图按项目区分，重要草稿在移动文件前应下载保留。

## 选择或添加自己的 HTML 案例

案例目录为此 skill 内的 [`assets/example/`](project-workboard/assets/example/)，在本仓库中的路径为 `project-workboard/assets/example/`。你可以替换内置案例，也可以把自己的 HTML 文件放到该目录，与现有案例并存；无需沿用内置文件名。

- **多个 HTML**：AI 列出可用文件，请用户选择。
- **只有一个 HTML**：AI 仍需请用户确认。
- **用户已明确指定文件**：直接使用该选择，不重复询问。
- **目录中没有 HTML**：AI 请用户添加或提供案例后再继续。
- **项目已有看板**：优先继续维护，无需每次工作都重新选择案例。

新版仅内置一个[通用导图案例](project-workboard/assets/example/workboard-map.html)，使用虚构的阶段、任务及多层子任务展示功能。整篇论文或某一章的修改均使用同一结构，按需要设置阶段与已有层级。

新增一层或改变既定层级组织，须由用户决定；智能体可提出建议。展开折叠不改变任务关系，无需逐次确认。任务状态、验收、证据及历史由智能体根据实际工作维护，浏览器操作只改变视图。数据结构与路径设置见[格式参考](project-workboard/references/workboard-format.cn.md)。

案例还用 10 项直属任务、3 个显式分类演示大量子任务的组织方式。某任务的直属子任务超过 8 个时，智能体会在规划或开始推进时建议分类，并先请用户确认；分类及成员明确记录，不随状态自动重排，也不改变真实父子关系和任务总数。

示例中的完成记录和证据链接均为演示，不代表真实验证。新建项目时替换项目名称、任务、历史、当前任务编号、材料路径和存储标识，另存到目标项目。

## 2.0 与已有项目

新版案例库默认只提供导图，不提供旧卡片／列布局切换。旧案例仍可从 [v1.1.0 稳定版](https://github.com/2505733155/project-workboard-repo/releases/tag/v1.1.0)或 Git 历史中获取。

更新技能后，已有看板继续按原格式维护，不会自动迁移或重置数据。若希望将旧看板迁为导图，应单独授权并保留编号、父子关系、依赖、状态语义、验收边界、结果、证据和历史。原文件及浏览器草稿／视图存储须在核验前保护；仅复制 HTML 不等于迁移了浏览器草稿。

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
    ├── SKILL.cn.md          # 供人阅读的中文译本
    ├── references/          # 按操作需要读取格式或经验指引
    │   ├── experience-reuse.md
    │   ├── experience-reuse.cn.md
    │   ├── workboard-format.md
    │   └── workboard-format.cn.md
    └── assets/
        └── example/         # 可替换、可并存的 HTML 案例
            └── workboard-map.html
```

仓库开发检查见 [tests/README.md](tests/README.md)。

## 致谢

感谢清华大学航空发动机研究院博士生刘晟奕同学，最早提出使用这一方法和思路，为本项目的形成提供了启发。

## 许可证

本项目采用 [MIT License](LICENSE)。
