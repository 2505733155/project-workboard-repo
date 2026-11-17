# Workboard Map Format

English (execution reference) | [Chinese reading translation](workboard-format.cn.md)

Read when creating or redesigning a map board, or changing its data structure or interactions. Continue maintaining an existing older board in its original format unless the user authorizes migration.

## Source and schema

Use [workboard-map.html](../assets/example/workboard-map.html) as the single bundled example. It is a standalone offline file with one authoritative JSON object in the script element with id workboard-data and type application/json. The engine and UI read that object; they do not scan project files, fetch another task list or write task data from browser actions.

Replace the fictional example with the actual authorized project. Keep JSON valid; escape less-than characters as \u003c inside JSON strings so text cannot terminate the script element. Use explicit fields, not task-number conventions:

| Field | Content |
| --- | --- |
| meta.title, meta.description | Project name and brief introduction |
| meta.version, meta.sample | Optional version label and fictional-sample badge; remove sample content for real work |
| meta.projectRoot | Project directory relative to the board file, with a trailing slash; use ./ for a root-level board and ../ for a board one directory below |
| meta.storageKey | Nonempty, stable, project-specific string for browser draft/view storage; choose a new key for each new project |
| meta.currentTaskId | Optional existing task ID; omit for project overview, do not guess one from task states |
| stages | Array of {id, name, environment, state, summary, acceptance, pending, evidence?}; state is an explicit phase sign-off record |
| tasks | Array of {id, stage, parent?, title, status, priority?, description?, acceptance?, deps?, verification?, evidence?, updatedAt?} |
| sources | Optional project materials as [{label, path}] |
| history, decisions | Optional arrays of {date, title, detail, stage?, task?, evidence?}; project overview exposes all records, phase/task details expose associated records |
| taskGroups | Optional explicit display categories; see the category rules below |
| statuses | Optional object mapping an existing status code to {label, kind}; kind is todo, doing, waiting or done |

IDs may be nonempty strings or finite numbers. String representations must be unique within stages and within tasks; a numeric ID and its identical string are the same reference. Stage, task and category namespaces are separate. Each task names an existing stage. An absent/null/empty parent means a top-level task under that stage; otherwise parent names an existing task in the same stage. deps is an array of task IDs, separate from parent. Missing materials and unfinished work stay recorded.

Default state codes are todo, doing, waiting and done. The skill defines their meaning; waiting requires both current scheduling and necessary user cooperation. Colors are derived from semantic kind: #465664, #215bd6, #8b5b0d and #21684b respectively, with white text. Custom labels/codes must have explicit semantic mappings. Phase acceptance is never inferred from children, percentages or colors.

The map validates duplicate IDs, missing stages/parents, parent cycles and cross-stage parents before drawing. It displays errors with the affected IDs and offers the raw records instead of silently repairing or discarding tasks. Unknown task states and malformed dependency arrays also require correction. Missing dependency/current-task references and dependency cycles produce visible warnings; dependency edges never become parent edges.


Declared text fields must be strings (or null/absent when optional); references must be valid IDs and evidence/history entries must be objects. Malformed field types enter the diagnostic view before any relationship or view initialization.

## Hierarchy and browsing

The hierarchy is project, stage, task and further explicitly registered subtasks, without a fixed business-depth limit. A single-stage project uses the same structure.

Adding a business level or changing the established hierarchy requires user confirmation. Adding tasks within already authorized scope and established levels follows that authorization. Expanding/collapsing is a view operation and does not need repeated confirmation.

Expanding a node immediately displays every direct display item from the relation index; for a categorized parent these are the categories, whose members remain available in full. Deeper children keep their own expansion state. Counts, visible children and right-side child lists use the same relation data. Search, dependency links and detail entries reveal necessary ancestors and locate existing nodes; they never change membership or create tasks.

Use map plus right-side details only. Tasks show their ID, title, status, priority, description, acceptance, direct children, dependencies, verification and evidence. Phases show requirements, explicit sign-off and unfinished items. Project overview gives materials, history and decisions. All long records remain readable. Narrow windows use a right-side overlay with controls to return to the canvas.

| Canvas input | Result |
| --- | --- |
| Wheel | Vertical pan; accept touchpad horizontal movement |
| Ctrl + wheel | Zoom around the pointer, preventing simultaneous page zoom inside the canvas |
| Shift + wheel | Horizontal pan, without counting both delta axes twice |
| Left- or right-button background drag | Pan; background context menus are suppressed, while controls, nodes and details keep their normal context menus |

Normalize pixel/line/page delta modes. Do not intercept scrolling in the detail panel or elsewhere on the page. Keep state text alongside color; selection outlines do not replace state fills. Buttons support keyboard activation.

## Explicit display categories

taskGroups is an optional array of {id, parent, stage, title, taskIds, description?, tone?}. Each category has its own ID, an existing task parent, the same stage as that parent, a nonempty title, and an explicitly ordered array of member task IDs. Optional tone is todo, doing, waiting or done; absent tone uses a neutral color. This is display styling, not a task state or acceptance result.

Category IDs have a separate namespace and must be unique by string representation within taskGroups. Categories never enter tasks or task totals and cannot be dependency targets. Keep each task's original parent, dependencies, state, acceptance and evidence intact. A category can only contain its parent's real direct subtasks, not descendants or other categories. Deeper real tasks may each have their own categories.

Once a parent has categories, every one of its direct tasks must appear exactly once across them. Duplicate/unknown/non-direct members, missing members, missing/wrong-stage parents, duplicate category IDs and malformed fields show diagnostics rather than silently repairing the display. Empty categories are allowed when the other categories still cover all tasks. Category and member order follows the explicit arrays.

Display paths become parent task, category, original child task. Expanding a parent exposes every category; expanding a category exposes all its members. Parent nodes distinguish category count from real direct-task count. Parent details retain both category entries and the entire real child-task list. Category details show their description, members and owning task, with no task acceptance or phase sign-off of their own. Search/current/dependency navigation reveals the necessary category path. Selection and browsing never change membership.

More than eight means nine or more real direct subtasks, not all descendants or displayed categories. At task planning (including a planned ninth child) or when starting relevant parent work, propose a useful classification and ask before adding the layer or changing the scheme. Keep the short approval/decline result in existing board history/decisions. Do not ask repeatedly after a decline without meaningful changes. Pending or declined grouping does not block other authorized work; keep the existing display until approval. The threshold is guidance for the agent, not a browser prompt or validity constraint; ungrouped parents with many tasks stay valid, and there is no mandatory maximum of eight per category.

After approval the agent maintains explicit membership under the agreed classification and existing task authorization, checking group placement when task state changes. The browser never automatically regroups tasks by state. Adding a real business level still follows the separate hierarchy-approval rule.

## Evidence and local storage

Resolve relative evidence paths against meta.projectRoot and the actual board URL, not a fixed directory depth. Keep the original readable path and a copy action. Offer file/http/https links where possible; do not treat an untested local link as verified access. Reject active schemes such as javascript and data. Local paths are literal filenames: characters such as #, ? and % are encoded as filename content. Use a complete http/https/file URL when URL fragments or query parameters are intended.

Browser storage uses project-workboard:v2:<storageKey>:draft and :view. Draft text can be typed and downloaded; it is not sent to an agent or written into task JSON. The view stores selection, expansion, zoom and pan. Stored entries with removed IDs fall back safely. Storage failures produce a message while browsing and draft download remain usable.

Do not reuse the example storageKey for a new project or delete other projects' keys. File URL storage behavior varies by browser and path; a new filename or browser may not share previous notes. Download important drafts before moving files.

## Existing projects

Updating the skill does not authorize rewriting an existing board, renumbering tasks or migrating browser storage. Obtain separate authorization for migration and agree the single authoritative source first.

An authorized migration must preserve task IDs, explicit parents, dependencies, state meanings, acceptance/sign-off boundaries, original results, evidence paths, decisions, history and unfinished work. Preserve original files and drafts/view storage until verified. Do not claim that copying HTML has transferred browser notes. This version provides no automatic migration utility.
