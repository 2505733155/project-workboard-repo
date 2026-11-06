# Git and GitHub beginner's guide

[简体中文](git-guide.md) | English · [Back to the project](../README.en.md)

This guide covers installing and updating Project Workboard, reporting problems, creating branches, and contributing changes. It focuses on VS Code and the GitHub website, with command-line alternatives. Choose either approach for each step; you do not need to perform both.

To try the skill first, follow the [README installation instructions](../README.en.md) and download a ZIP. Git is optional for that route. Cloning with Git makes future updates easier.

## Prepare your tools

1. Install Git for your system from the [official Git website](https://git-scm.com/downloads). Reopen VS Code afterward. Run `git --version` in a terminal; a version number means Git is available.
2. Install and open [VS Code](https://code.visualstudio.com/). Use **View → Command Palette**, or `Ctrl+Shift+P` on Windows/Linux and `Cmd+Shift+P` on macOS.
3. Downloading a public repository usually requires no GitHub account. To open issues, fork a repository, or submit pull requests, register and sign in at [GitHub](https://github.com/). If VS Code asks you to sign in when pushing, follow its browser sign-in flow.

Before your first commit, Git needs an author name and email address. Open **Terminal → New Terminal** in the cloned repository folder, replace the example values with your own, and run these commands. `--local` applies the settings only to this repository:

```sh
git config --local user.name "Your name"
git config --local user.email "Your email address"
```

## Understand the terms

| Term | What it means here |
| --- | --- |
| Git | A tool for recording local file versions, branches, and commits |
| GitHub | A website for hosting remote repositories, discussing issues, and reviewing changes |
| Clone | Download a repository and its version history to your computer |
| Fork | Create a repository copy under your own GitHub account that you can modify |
| Branch | A separate line of work for a change, such as `docs/clarify-installation` |
| Commit | Save a version of selected local changes with a message; it has not been uploaded yet |
| Push / Pull | Upload local commits to a remote / retrieve and integrate remote changes locally |
| Issue | Report a problem, suggest an improvement, or start a discussion with maintainers |
| Pull request (PR) | Ask maintainers to review and merge changes from your branch into the original repository |

## Install

### Clone with VS Code

1. Open the Command Palette and choose **Git: Clone**.
2. Enter `https://github.com/2505733155/project-workboard-repo.git`.
3. Choose a parent folder for the source checkout, then open the cloned repository. If VS Code asks whether you trust the authors, decide based on your knowledge of the source.
4. In your system's file manager, find the inner `project-workboard/` directory and copy that complete directory into the skill location recognized by your AI tool. See the [README installation directory table](../README.en.md#installation).
5. Refresh or restart the AI tool as required, confirm that `project-workboard` appears in its skill list, and follow [Getting started](../README.en.md#getting-started) to create a project board.

Alternatively, open a terminal in the parent folder where you keep source repositories and run:

```sh
git clone https://github.com/2505733155/project-workboard-repo.git
cd project-workboard-repo
git status
```

Then complete steps 4 and 5 above. **Cloning the repository and installing the skill are separate steps.** For example, a Codex installation using `.agents` looks like this:

```text
Source checkout: any-source-folder/project-workboard-repo/
Directory to copy: project-workboard/ inside the checkout
Installed files: ~/.agents/skills/project-workboard/SKILL.md
                 ~/.agents/skills/project-workboard/assets/example/...
```

`~` means your home directory. Avoid adding an extra `project-workboard-repo/` level, and do not copy only `SKILL.md`. Save generated project boards in your own thesis or project directory for that project's use.

## Update

Updating has two parts: update the source checkout, then copy the updates into the installed skill.

### Update the source checkout

Open the previously cloned repository in VS Code and check **Source Control** for uncommitted changes. If you have no changes of your own, use **… → Pull**. Menu labels vary by version and language; **Git: Pull** in the Command Palette is another option.

The equivalent terminal workflow, run from the repository root, is:

```sh
git status
git switch main
git pull --ff-only
```

`git status` should show a clean working tree. If you have edits, back them up and decide how to preserve or merge them before switching branches or pulling. `--ff-only` allows only a direct fast-forward update. If branches have diverged, conflicts occur, or a command fails, inspect the cause before continuing; do not force an overwrite to bypass your changes. If this checkout is your own fork, synchronize the fork as described under “Contribute again” below first.

### Update the installed copy

1. Back up the installed `project-workboard/` directory to another location, preserving custom examples and edits to the original files.
2. Copy the contents of `project-workboard/` from the updated checkout into the actual installation directory, replacing official files with their newer versions. Keep additional custom HTML examples. If you edited an official file with the same name, compare and merge your changes first.
3. Refresh or restart the AI tool and confirm that it can read the skill and examples.

**`git pull` updates the current source checkout; it does not automatically update a skill installed elsewhere.** Existing thesis or project boards are maintained in their respective projects; continue using those boards after updating the skill.

If you originally downloaded a ZIP, the extracted directory has no Git history and cannot be updated with `git pull`. Download a new ZIP and update the installed copy as above, or clone into a separate source directory and use Git for future updates.

## Open an issue

You do not need a branch or a file change to report a problem or suggest an improvement.

1. Open the project's [Issues page](https://github.com/2505733155/project-workboard-repo/issues) and search for an existing report first.
2. Sign in to GitHub, click **New issue**, and follow the template or blank form offered by the page.
3. Use a specific title, such as “Claude Code does not recognize the installed skill.”
4. For a bug, include your AI tool and version, operating system, installation method, reproduction steps, expected result, and actual result. Add error text or relevant screenshots when helpful. For an improvement, describe your use case, the difficulty, and the desired outcome.
5. Follow replies and provide additional information if requested. Once resolved, explain the outcome and close your issue if appropriate.

## Fork, create a branch, and submit a pull request

Most users do not have permission to push directly to the original repository. The full contribution workflow is: **fork the repository → clone your fork → create a branch → edit and commit → push to your fork → open a PR against the original repository**.

### Create your fork

1. Open the [original repository](https://github.com/2505733155/project-workboard-repo), click **Fork**, and create the copy under your own account.
2. On your fork's page, click **Code** and copy its HTTPS URL.
3. Use **Git: Clone** in VS Code to clone that URL and open the resulting folder. If you already cloned the original repository, keep your fork checkout in another location so they are easy to distinguish.

Replace `YOUR-USERNAME` below with your GitHub username. Run the commands in a different parent folder to avoid an existing directory with the same name:

```sh
git clone https://github.com/YOUR-USERNAME/project-workboard-repo.git
cd project-workboard-repo
git remote -v
```

Confirm that `origin` points to your fork, rather than the original repository owned by `2505733155`. If you renamed the repository while forking, use the URL copied from **Code** and the matching directory name.

### Create a branch and edit

Make sure your fork is synchronized with the original repository, then create a branch from your local `main`. In VS Code, click the branch name in the lower-left corner, choose **Create new branch**, and enter a name such as `docs/clarify-installation`.

Equivalent commands:

```sh
git switch main
git pull --ff-only
git switch -c docs/clarify-installation
```

Edit files on this branch. Keep each PR focused on one change, such as clarifying installation or adding an example. Use these locations:

| Change | File location |
| --- | --- |
| Project overview | `README.md`, `README.en.md` |
| Beginner's guide | `docs/git-guide.md`, `docs/git-guide.en.md` |
| Skill instructions read by the AI | `project-workboard/SKILL.md` |
| HTML examples | `project-workboard/assets/example/` |

Keep Chinese and English documentation aligned where possible. After adding an example, open it in a browser to check its display and interactions, and describe its use case in the README. Include only files needed for the change.

### Commit and push

1. In VS Code's **Source Control**, open each changed file and review its diff.
2. Click **+** next to the intended files to stage them. The staging area determines which files go into the commit.
3. Enter a message such as `docs: clarify installation` and click **Commit**. If prompted for a name or email, configure your author identity as described earlier.
4. Click **Publish Branch** for a new branch, or **Push** for later changes. Confirm that the destination is your fork and complete GitHub sign-in if prompted.

The example below assumes you edited both READMEs; substitute the actual file paths for your change:

```sh
git diff
git add README.md README.en.md
git diff --cached
git commit -m "docs: clarify installation"
git push -u origin docs/clarify-installation
```

### Open the PR on GitHub

After pushing, open your fork on GitHub and click **Compare & pull request**. Alternatively, use **Pull requests → New pull request → compare across forks** in the original repository.

Confirm that the base repository is `2505733155/project-workboard-repo` and its base branch is `main`, while the head is your fork's `docs/clarify-installation` branch. Explain the problem, your changes, and how you checked them. If relevant, write `Closes #NUMBER` to link an issue. Review all changes under **Files changed**, then click **Create pull request**.

Maintainers may request revisions. Edit, commit, and push on the same local branch; the existing PR updates automatically. You do not need another PR. A submitted PR still needs maintainer review and merging before it becomes part of the original repository.

## Contribute again

Before your next contribution, keep your local working tree clean and use **Sync fork → Update branch** on your GitHub fork to synchronize its `main` with the original repository. If GitHub reports conflicts, resolve them before continuing; do not discard your commits to bypass the conflict.

Then pull the updated fork into your local checkout and create a new branch for the next change:

```sh
git switch main
git pull --ff-only
git switch -c docs/improve-examples
```

In general, keep your fork's `main` for synchronizing with the original repository and use a separate branch for each contribution. If a push is rejected, inspect the signed-in account, the `origin` URL, and branch status before continuing. Do not force-push over existing history.

For more background, see GitHub's documentation on [forking a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) and [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).
