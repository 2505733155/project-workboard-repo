# Development checks

The installed skill and its offline HTML need no Node.js, Python, server or network connection. These tools are for repository development only.

Run the embedded engine tests (Node.js):
```text
node --test tests/workboard-map.test.cjs
```

Run real Chromium interaction checks with Python and Playwright:
```text
python -m pip install playwright
python tests/browser-workboard.py --browser "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

Use an existing Edge/Chrome executable. No Playwright browser download is required. --artifacts selects an external screenshot/download directory (default: operating-system temp directory). Tests open generated local files in an isolated browser context; they do not modify installed skills or real project files.

Optional local scale test:
```text
python tests/browser-workboard.py --snapshot <path-to-local-handoff-html>
```

The optional snapshot must contain the original JSON script with stages/tasks. It is injected only into temporary browser fixtures. Do not add real project snapshots or screenshots containing project data to the public repository.

The grouped and ungrouped browser fixtures use separate project storage keys so persisted expansion cannot contaminate fresh-view assertions. Group tests check explicit membership, semantic parents, complete child lists, counts and navigation; 8/9 ungrouped children remain valid.

The Node suite checks hierarchy, missing/cyclic relations, layout, status mapping, evidence roots and input calculations. Browser checks exercise actual rendering, wheel/drag/keyboard, right/narrow details, drafts, view persistence, denied/corrupt storage and escaped content. Programmatic Chromium inputs do not replace hands-on checks for every physical mouse/touchpad/browser combination.
