# Git 与 GitHub 新手指南

简体中文 | [English](git-guide.en.md) · [返回项目首页](../README.md)

这份指南介绍如何安装和更新 Project Workboard，以及如何反馈问题、创建分支和提交改进。以 VS Code 和 GitHub 网页操作为主，命令行步骤作为另一种做法；同一步骤任选一种方式即可。

只想先体验，可以按 [README 的安装说明](../README.md) 下载 ZIP，无需安装 Git。希望方便地获取后续更新，建议使用下面的 Git 克隆方式。

## 准备工具

1. 从 [Git 官网](https://git-scm.com/downloads) 安装适合自己系统的 Git。安装后重新打开 VS Code；在终端运行 `git --version`，出现版本号即表示可用。
2. 安装并打开 [VS Code](https://code.visualstudio.com/)。命令面板可用菜单 **查看 → 命令面板** 打开；Windows/Linux 快捷键为 `Ctrl+Shift+P`，macOS 为 `Cmd+Shift+P`。
3. 下载公开仓库通常无需 GitHub 账号。提交 Issue、Fork 或 Pull Request 时，需要先在 [GitHub](https://github.com/) 注册并登录。VS Code 推送时若提示登录，按提示在浏览器中完成。

第一次提交修改时，Git 需要作者姓名和邮箱。在克隆后的仓库文件夹中打开 **终端 → 新建终端**，将下面的示例替换为自己的信息后运行；`--local` 表示只设置当前仓库：

```sh
git config --local user.name "你的名字"
git config --local user.email "你的邮箱"
```

## 先认识几个词

| 名称 | 在本项目中的意思 |
| --- | --- |
| Git | 记录本地文件版本、分支和提交的工具 |
| GitHub | 托管远程仓库、讨论问题和审阅改动的网站 |
| Clone（克隆） | 将远程仓库及其版本历史下载到本地 |
| Fork | 在自己的 GitHub 账号下创建一份可自行修改的仓库副本 |
| Branch（分支） | 为一项改动建立的独立工作线，例如 `docs/clarify-installation` |
| Commit（提交） | 给一组本地修改保存版本并附上说明；还没有上传到 GitHub |
| Push / Pull（推送 / 拉取） | 将本地提交上传到远程 / 将远程更新取回并整合到本地 |
| Issue | 向维护者报告问题、提出建议或发起讨论 |
| Pull Request（PR，拉取请求） | 请维护者审阅并将自己分支上的改动合并进原仓库 |

## 安装

如果希望让智能体协助安装，可以直接使用 [README 中的安装提示词](../README.md#通过智能体安装)。下面介绍使用 Git 克隆和安装的具体步骤。

### 用 VS Code 克隆

1. 打开命令面板，选择 **Git: Clone（克隆）**。
2. 输入仓库地址：`https://github.com/2505733155/project-workboard-repo.git`。
3. 选择用于存放源码的父文件夹，克隆完成后打开仓库。VS Code 可能显示“是否信任作者”等提示，按你对源码的了解决定。
4. 在系统文件管理器中找到仓库内层的 `project-workboard/`，将整个子目录复制到 AI 工具识别的技能目录中。各工具的安装位置见 [README 安装目录表](../README.md#安装)。
5. 按 AI 工具要求刷新或重启会话，在技能列表中确认能找到 `project-workboard`，再按 [开始使用](../README.md#开始使用) 创建项目看板。

也可以在用于存放源码的父文件夹中打开终端，执行：

```sh
git clone https://github.com/2505733155/project-workboard-repo.git
cd project-workboard-repo
git status
```

之后同样需要完成第 4、5 步。**克隆仓库和安装技能是两个步骤。** 例如使用 Codex 的 `.agents` 安装目录时，关系如下：

```text
源码仓库：任意源码目录/project-workboard-repo/
需要复制的内容：源码仓库中的 project-workboard/
安装结果：~/.agents/skills/project-workboard/SKILL.md
          ~/.agents/skills/project-workboard/assets/example/...
```

`~` 表示用户主目录。避免多套一层 `project-workboard-repo/`，也不要只复制 `SKILL.md`。生成的项目看板保存到自己的论文或项目目录中，供该项目使用。

## 更新

更新分为“更新源码仓库”和“同步安装副本”两步。

### 更新源码仓库

在 VS Code 中打开原先克隆的仓库，先在 **源代码管理** 中检查有无未提交的修改。没有自己的改动时，从 **… → 拉取（Pull）** 获取更新。菜单文字可能随版本和语言不同；也可使用命令面板中的 **Git: Pull**。

终端中的对应做法如下。在仓库根目录执行：

```sh
git status
git switch main
git pull --ff-only
```

`git status` 应显示工作区干净；若有自己的修改，先备份并决定如何保留或合并，再继续切换和拉取。`--ff-only` 要求只做直接前进的更新；遇到分支分叉、冲突或报错时，先查看原因，不要用强制覆盖来跳过自己的改动。如果克隆的是自己的 Fork，请先按下文“继续参与改进”同步 Fork。

### 同步安装副本

1. 将已安装的 `project-workboard/` 备份到另一个位置，保留自定义案例和对原文件的修改。
2. 将更新后的仓库中 `project-workboard/` 的内容复制到实际安装目录，同名官方文件使用新版本。保留额外添加的 HTML 案例；若自己修改过同名官方文件，先比较并合并改动。
3. 刷新或重启 AI 工具，确认技能和案例可读取。

**`git pull` 只更新当前源码仓库，不会自动更新另一个位置的安装副本。** 已生成的论文或项目看板也由各自项目维护，更新技能后仍继续使用原看板。

如果最初下载的是 ZIP，解压目录没有 Git 版本历史，不能直接 `git pull`。可重新下载 ZIP 后按上述方式同步安装副本，或重新克隆到另一个源码目录，以后使用 Git 更新。

## 提交 Issue

反馈问题和提出建议不需要创建分支或修改文件。

1. 打开项目的 [Issues 页面](https://github.com/2505733155/project-workboard-repo/issues)，先搜索是否已有相同问题。
2. 登录 GitHub 后点击 **New issue**，按页面给出的模板或空白表单填写。
3. 用明确的标题描述问题，例如“使用 Claude Code 安装后未识别到技能”。
4. 问题报告写清使用的 AI 工具及版本、操作系统、安装方式、复现步骤、预期结果和实际结果；必要时附报错文字或相关截图。功能建议则说明使用场景、遇到的困难和希望达到的效果。
5. 提交后留意维护者的回复，补充所需信息；问题解决后可说明结果并关闭自己的 Issue。

## Fork、创建分支并提交 Pull Request

普通使用者通常没有向原仓库直接推送的权限。参与改进的完整过程是：**Fork 原仓库 → 克隆自己的 Fork → 创建分支 → 修改并提交 → 推送到自己的 Fork → 向原仓库提出 PR**。

### 创建自己的 Fork

1. 打开 [原仓库](https://github.com/2505733155/project-workboard-repo)，点击右上角 **Fork**，将副本创建在自己的账号下。
2. 在自己的 Fork 页面点击 **Code**，复制 HTTPS 地址。
3. 使用 VS Code 的 **Git: Clone** 克隆这个地址，并打开克隆后的文件夹。若之前已克隆原仓库，可将自己的 Fork 克隆到另一个位置，方便区分。

终端示例中的 `YOUR-USERNAME` 必须替换为自己的 GitHub 用户名；在另一个父文件夹中执行，避免与已有同名目录冲突：

```sh
git clone https://github.com/YOUR-USERNAME/project-workboard-repo.git
cd project-workboard-repo
git remote -v
```

确认 `origin` 指向自己的 Fork，而不是 `2505733155` 的原仓库。Fork 时若改了仓库名称，使用 **Code** 按钮复制的实际地址和对应目录名。

### 创建分支并修改

先确认 Fork 已同步原仓库，再从本地 `main` 创建分支。在 VS Code 中点击左下角分支名称，选择 **创建新分支（Create new branch）**，输入本次改动的名称，例如 `docs/clarify-installation`。

对应命令：

```sh
git switch main
git pull --ff-only
git switch -c docs/clarify-installation
```

在这个分支上修改文件。一项 PR 尽量围绕一件事，例如补充安装说明或增加一个案例。修改位置可参考：

| 改动内容 | 文件位置 |
| --- | --- |
| 首页说明 | `README.md`、`README.en.md` |
| 新手指南 | `docs/git-guide.md`、`docs/git-guide.en.md` |
| AI 读取的技能规则 | `project-workboard/SKILL.md` |
| HTML 案例 | `project-workboard/assets/example/` |

修改说明时尽量同步中英文版本；添加案例后，用浏览器打开检查显示和交互，并在 README 中补充适用场景。只提交这项改动需要的文件。

### 提交并推送

1. 在 VS Code 的 **源代码管理** 中点开修改过的文件，逐一查看差异。
2. 点击目标文件旁的 **+** 将其加入暂存区。暂存区决定本次提交包含哪些文件。
3. 填写提交说明，例如 `docs: 补充安装说明`，点击 **提交（Commit）**。如提示缺少姓名或邮箱，按前文设置作者信息。
4. 点击 **发布分支（Publish Branch）**；后续修改则使用 **推送（Push）**。确认目标是自己的 Fork，并按提示完成 GitHub 登录。

以下以修改两份 README 为例；实际使用时把文件名替换为本次要提交的路径：

```sh
git diff
git add README.md README.en.md
git diff --cached
git commit -m "docs: 补充安装说明"
git push -u origin docs/clarify-installation
```

### 在 GitHub 创建 PR

推送后，打开自己的 Fork 页面，点击 **Compare & pull request**；也可从原仓库的 **Pull requests → New pull request → compare across forks** 进入。

确认目标为原仓库 `2505733155/project-workboard-repo` 的 `main`，来源为自己 Fork 的 `docs/clarify-installation` 分支。填写改动解决了什么问题、修改内容和检查方法；若关联 Issue，可写 `Closes #编号`。检查 **Files changed** 中的全部差异，然后点击 **Create pull request**。

维护者可能提出修改建议。在同一个本地分支继续修改、提交并推送，新提交会自动进入已有 PR，无需重新创建。PR 需要维护者审阅和合并，提交成功不等于已并入原仓库。

## 继续参与改进

下一次贡献前，先保持本地工作区干净，在自己的 GitHub Fork 页面选择 **Sync fork → Update branch** 同步原仓库的 `main`。若 GitHub 提示存在冲突，先解决冲突，再继续；不要选择丢弃自己提交的操作来绕过问题。

然后回到本地 Fork，拉取更新，并为下一项改动创建一个新分支：

```sh
git switch main
git pull --ff-only
git switch -c docs/improve-examples
```

一般保持 Fork 的 `main` 用于同步原仓库，每项改动使用各自分支。推送被拒绝时，先检查登录账号、`origin` 地址和分支状态，不使用强制推送覆盖已有历史。

需要进一步了解时，可阅读 [GitHub 的 Fork 说明](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)和 [Pull Request 说明](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)。
