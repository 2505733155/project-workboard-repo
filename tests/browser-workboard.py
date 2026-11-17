"""Real Chromium tests for the standalone file. Development dependency: playwright."""
import argparse, json, os, re, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument("--browser",default=os.environ.get("WORKBOARD_BROWSER",r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
parser.add_argument("--artifacts",default=str(Path(tempfile.gettempdir())/"workboard-v2-evidence"))
parser.add_argument("--snapshot",help="Optional original local handoff HTML; never copied to tracked fixtures.")
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
html=(root/"project-workboard/assets/example/workboard-map.html").read_text(encoding="utf-8")
match=re.search(r'(<script id="workboard-data" type="application/json">)([\s\S]*?)(</script>)',html)
if not match:
    raise AssertionError("The standalone page needs its canonical workboard-data JSON.")
data=json.loads(match[2])
artifacts=Path(args.artifacts);artifacts.mkdir(parents=True,exist_ok=True)
checks=[]
def ok(label): checks.append(label);print("PASS",label,flush=True)
def template(board):
    encoded=json.dumps(board,ensure_ascii=False).replace("</","<\\/")
    return html[:match.start(2)]+encoded+html[match.end(2):]
with tempfile.TemporaryDirectory(prefix="workboard-browser-") as folder, sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.browser,headless=True)
    context=browser.new_context(viewport={"width":1440,"height":1000},accept_downloads=True)
    errors=[]
    context.on("page",lambda page:page.on("pageerror",lambda error:errors.append(str(error))))
    def load(board=None,script=None,name="test"):
        page=context.new_page()
        if script:page.add_init_script(script)
        path=Path(folder)/(name+".html")
        path.write_text(html if board is None else template(board),encoding="utf-8")
        page.goto(path.as_uri());page.wait_for_selector("#project-title")
        return page
    def go(page,key):
        page.locator("#search").fill(key.split(":",1)[-1])
        page.locator('[data-search="'+key+'"]').click()
    def transform(page):
        return page.locator("#world").evaluate("(e)=>{const m=new DOMMatrix(getComputedStyle(e).transform);return {x:m.e,y:m.f,scale:m.a}}")
    capture="const parse=JSON.parse;JSON.parse=function(...a){const d=parse(...a);if(d&&Array.isArray(d.tasks)&&Array.isArray(d.stages)){window.testBoard=d;window.testBoardBefore=JSON.stringify(d)}return d;}"
    grouped_board=json.loads(json.dumps(data))
    for n in [8,9,10]:
        if not any(t["id"]=="collect-"+str(n) for t in grouped_board["tasks"]):
            grouped_board["tasks"].append({"id":"collect-"+str(n),"stage":"prepare","parent":"collect","title":"Extra "+str(n),"status":"todo","deps":["collect-1"]})
    grouped_board["taskGroups"]=[
        {"id":"materials","parent":"collect","stage":"prepare","title":"材料准备","description":"明确记录的材料分类","taskIds":["collect-1","collect-4","collect-8"]},
        {"id":"checks","parent":"collect","stage":"prepare","title":"核对与确认","taskIds":["collect-2","collect-3","collect-6","collect-9"]},
        {"id":"summary","parent":"collect","stage":"prepare","title":"归档与汇总","taskIds":["collect-5","collect-7","collect-10"]}
    ]
    groups=load(grouped_board,script=capture,name="groups")
    groups.locator("#overview").click();go(groups,"task:collect")
    groups.locator('[data-toggle="task:collect"]').click()
    assert groups.locator('[data-node^="group:"]').count()==3
    assert groups.locator('[data-node="task:collect-1"]').count()==0
    assert "3 类" in groups.locator('[data-node="task:collect"] .node-meta').inner_text()
    assert "10 项" in groups.locator('[data-node="task:collect"] .node-meta').inner_text()
    assert groups.locator('#detail [data-go^="group:"]').count()==3
    assert groups.locator('#detail [data-go^="task:collect-"]').count()==10
    go(groups,"group:materials")
    assert "任务分类" in groups.locator("#detail").inner_text()
    assert "不计入任务总数" in groups.locator("#detail").inner_text()
    assert groups.locator('#detail [data-go^="task:collect-"]').count()==3
    groups.locator('[data-toggle="group:materials"]').click()
    for id in ["collect-1","collect-4","collect-8"]:assert groups.locator('[data-node="task:'+id+'"]').count()==1
    assert groups.locator('[data-node="task:collect-2"]').count()==0
    go(groups,"task:collect-2-1-a")
    assert groups.locator('[data-node="group:checks"]').count()==1
    assert groups.locator('[data-node="task:collect-2-1-a"]').count()==1
    go(groups,"task:collect-9")
    groups.locator('#detail [data-go="task:collect-1"]').click()
    assert groups.locator("#detail").get_attribute("data-selected")=="task:collect-1"
    assert groups.locator('[data-node="task:collect-1"]').count()==1
    groups.locator("#focus-current").click()
    assert groups.locator("#detail").get_attribute("data-selected")=="task:collect-2"
    go(groups,"group:summary");groups.wait_for_timeout(200);groups.reload();groups.wait_for_selector("#project-title")
    assert groups.locator("#detail").get_attribute("data-selected")=="group:summary"
    assert groups.evaluate("JSON.stringify(window.testBoard)===window.testBoardBefore")
    groups.screenshot(path=str(artifacts/"groups.png"),full_page=True)
    groups.set_viewport_size({"width":420,"height":880});go(groups,"group:checks")
    assert groups.locator("#detail").is_visible()
    assert groups.locator("#detail").bounding_box()["x"]>0
    assert groups.locator('#detail [data-go^="task:collect-"]').count()==4
    groups.screenshot(path=str(artifacts/"groups-narrow.png"),full_page=True)
    ok("explicit groups, real counts, all members, dependency/current reveal and group view restore")
    malformed_group=json.loads(json.dumps(grouped_board));malformed_group["taskGroups"][0]["taskIds"].pop()
    broken=load(malformed_group,name="missing-group-member")
    assert broken.locator("#diagnostics").is_visible()
    assert "collect-8" in broken.locator("#diagnostics").inner_text()
    assert broken.locator("[data-node]").count()==0
    ok("unassigned category members diagnose without hiding records")
    # Preserve the pre-group seven-child regression as an explicitly ungrouped fixture.
    legacy=json.loads(json.dumps(data));legacy.pop("taskGroups",None)
    legacy["meta"]["storageKey"]+="-ungrouped-regression"
    legacy["tasks"]=[t for t in legacy["tasks"] if t["id"] not in ["collect-8","collect-9","collect-10"]]
    page=load(legacy,script=capture,name="main")
    original=page.locator("#workboard-data").text_content()
    go(page,"task:collect")
    toggle=page.locator('[data-toggle="task:collect"]')
    if toggle.get_attribute("aria-expanded")=="true":toggle.click()
    toggle.click()
    for n in range(1,8):assert page.locator('[data-node="task:collect-'+str(n)+'"]').count()==1
    assert page.locator('[data-node="task:collect-2-1"]').count()==0
    assert page.locator('#detail [data-go^="task:collect-"]').count()==7
    ok("all seven children and matching detail count; deeper nodes folded")
    toggle.focus();toggle.press("Space")
    assert toggle.get_attribute("aria-expanded")=="false"
    toggle.press("Space")
    assert toggle.get_attribute("aria-expanded")=="true"
    page.locator('[data-node="task:collect-2"] .node-main').focus()
    page.locator('[data-node="task:collect-2"] .node-main').press("Enter")
    assert page.evaluate("document.activeElement.dataset.select")=="task:collect-2"
    ok("keyboard toggles exactly once and node selection retains focus")
    go(page,"task:collect-2-1-a")
    assert page.locator('[data-node="task:collect-2-1-a"]').count()==1
    assert page.locator("#detail").inner_text().find("collect-2-1-a")>=0
    assert page.locator('[data-node="task:collect-7"]').count()==1
    ok("search reveals deep path without hiding siblings")
    assert page.locator("#workboard-data").text_content()==original
    page.locator("#overview").click()
    for label in ["历史","决策","材料"]:assert label in page.locator("#detail").inner_text()
    assert page.locator("#detail a[data-evidence]").count()>0
    page.locator('#detail [data-go="stage:prepare"]').click()
    assert "尚未签收" in page.locator("#detail").inner_text()
    ok("project materials/history/decisions and explicit phase acceptance remain accessible")
    page.locator("#fit").click()
    box=page.locator("#canvas").bounding_box()
    cx,cy=box["x"]+box["width"]/2,box["y"]+box["height"]/2
    page.mouse.move(cx,cy)
    before=transform(page);page.mouse.wheel(0,90);page.wait_for_timeout(100);after=transform(page)
    assert abs(after["y"]-(before["y"]-90))<1
    assert abs(after["scale"]-before["scale"])<1e-5
    before=after
    page.keyboard.down("Shift");page.mouse.wheel(0,60);page.keyboard.up("Shift");page.wait_for_timeout(100);after=transform(page)
    assert abs(after["x"]-(before["x"]-60))<1
    assert abs(after["y"]-before["y"])<1
    before=after
    page.keyboard.down("Control");page.mouse.wheel(0,-100);page.keyboard.up("Control");page.wait_for_timeout(100);after=transform(page)
    anchorx=box["width"]/2;anchory=box["height"]/2
    assert after["scale"]>before["scale"]
    assert abs((anchorx-before["x"])/before["scale"]-(anchorx-after["x"])/after["scale"])<1
    assert abs((anchory-before["y"])/before["scale"]-(anchory-after["y"])/after["scale"])<1
    ok("real wheel: vertical, Shift horizontal and Ctrl pointer-centered zoom")
    # Use a blank corner, away from nodes.
    page.locator("#overview").click();page.locator("#fit").click()
    x,y=box["x"]+15,box["y"]+15
    before=transform(page);page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+45,y+30,steps=4);page.mouse.up();after=transform(page)
    assert abs(after["x"]-before["x"]-45)<1
    assert abs(after["y"]-before["y"]-30)<1
    ok("background drag pans the canvas")
    page.evaluate("window.rightMenuEvents=[];document.addEventListener('contextmenu',e=>window.rightMenuEvents.push({prevented:e.defaultPrevented,target:e.target.id}))")
    before=transform(page);page.mouse.move(x,y);page.mouse.down(button="right");page.mouse.move(x+55,y+35,steps=5);page.mouse.up(button="right")
    after=transform(page)
    assert abs(after["x"]-before["x"]-55)<1
    assert abs(after["y"]-before["y"]-35)<1
    assert not page.locator("#canvas").evaluate("(e)=>e.classList.contains('dragging')")
    assert page.evaluate("window.rightMenuEvents.length>0 && window.rightMenuEvents.every(e=>e.prevented)")
    page.locator('#detail h2').click(button="right")
    assert page.evaluate("window.rightMenuEvents.at(-1).prevented") is False
    page.keyboard.press("Escape")
    page.locator('[data-node="project"] .node-main').click(button="right")
    assert page.evaluate("window.rightMenuEvents.at(-1).prevented") is False
    page.keyboard.press("Escape")
    ok("right-background drag pans without a context menu; detail/node menus stay available")
    go(page,"task:collect-2")
    before=transform(page)
    page.locator("#detail").hover();page.mouse.wheel(0,500);page.wait_for_timeout(100)
    assert transform(page)==before
    assert page.locator("#detail").evaluate("(e)=>e.scrollTop")>0
    ok("right detail scroll is independent of canvas")
    page.locator("#scratch-toggle").click()
    draft="草稿验证：内容不会写回任务 JSON。"
    page.locator("#draft").fill(draft);page.wait_for_timeout(350)
    with page.expect_download() as dl:page.locator("#download-draft").click()
    downloaded=artifacts/"draft-test.txt";dl.value.save_as(downloaded)
    assert downloaded.read_text(encoding="utf-8-sig")==draft
    page.locator("#scratch-close").click()
    expected=page.locator("#detail").get_attribute("data-selected")
    page.reload();page.wait_for_selector("#project-title")
    assert page.locator("#detail").get_attribute("data-selected")==expected
    page.locator("#scratch-toggle").click();assert page.locator("#draft").input_value()==draft
    page.locator("#scratch-close").click()
    assert page.locator("#workboard-data").text_content()==original
    ok("draft persistence/download and selected-view restore do not mutate JSON")
    assert page.evaluate("JSON.stringify(window.testBoard)===window.testBoardBefore")
    stored=page.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('project-workboard:v2:'))")
    assert stored and all(data["meta"]["storageKey"] in key for key in stored)
    go(page,"task:collect");page.locator("#fit").click();page.screenshot(path=str(artifacts/"wide.png"),full_page=True)
    page.set_viewport_size({"width":420,"height":880});go(page,"task:collect-2")
    assert page.locator("#detail").is_visible()
    assert page.locator("#detail").bounding_box()["x"]>=0
    assert page.locator("#detail").bounding_box()["x"]>0
    page.screenshot(path=str(artifacts/"narrow.png"),full_page=True)
    page.locator("#close-detail").click()
    assert not page.locator("#detail").is_visible()
    page.locator("#open-detail").click();assert page.locator("#detail").is_visible()
    ok("narrow right overlay opens/closes without a bottom layout")
    denied=load(script="Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}})",name="denied")
    assert denied.locator('[data-node="project"]').count()==1
    denied.locator("#scratch-toggle").click();denied.locator("#draft").fill("still usable")
    assert denied.locator("#draft").input_value()=="still usable"
    ok("unavailable storage leaves browsing and draft typing usable")
    corrupt=load(script="localStorage.setItem('project-workboard:v2:"+data["meta"]["storageKey"]+":view','{bad')",name="corrupt")
    assert corrupt.locator('[data-node="project"]').count()==1
    assert "视图" in corrupt.locator("#storage-status").inner_text()
    ok("corrupt saved view visibly falls back")
    for field in ["parent","stage","deps","current","title","record"]:
        malformed=json.loads(json.dumps(data))
        strange={"toString":None}
        if field in ["parent","stage"]:malformed["tasks"][1][field]=strange
        elif field=="deps":malformed["tasks"][1]["deps"]=[strange]
        elif field=="current":malformed["meta"]["currentTaskId"]=strange
        elif field=="title":malformed["meta"]["title"]=strange
        else:malformed["history"]=[{"title":strange,"detail":"invalid title"}]
        problem=load(malformed,name="malformed-"+field)
        assert problem.locator("#diagnostics").is_visible(),field
        assert problem.locator("#raw-data").text_content(),field
        assert problem.locator("[data-node]").count()==0
    ok("malformed relation/metadata/record types diagnose instead of crashing")
    custom=json.loads(json.dumps(data));custom["tasks"][0]["parent"]="missing-parent"
    bad=load(custom,name="invalid")
    assert bad.locator("#diagnostics").is_visible()
    assert "missing-parent" in bad.locator("#diagnostics").inner_text()
    assert bad.locator("[data-node]").count()==0
    assert bad.locator("#raw-data").text_content()
    ok("invalid hierarchy produces actionable diagnosis, not a repaired tree")
    hostile=json.loads(json.dumps(data))
    hostile["tasks"][0]["title"]='<img src=x onerror="window.bad=1">'
    hostile["sources"]=[{"label":"unsafe","path":"javascript:window.bad=1"}]
    safe=load(hostile,name="hostile");safe.locator("#overview").click()
    assert safe.locator("#detail a[href^='javascript:']").count()==0
    assert safe.locator("#nodes img").count()==0
    assert safe.evaluate("window.bad||0")==0
    ok("task text is escaped and active evidence URLs are not linked")
    # Same file URL, new project key: neither project may overwrite the other's notes.
    isolated=load(name="isolation")
    isolated.evaluate("localStorage.setItem('legacy-workboard-draft','preserve me')")
    isolated.locator("#scratch-toggle").click();isolated.locator("#draft").fill("project A")
    other=json.loads(json.dumps(data));other["meta"]["storageKey"]="separate-project"
    (Path(folder)/"isolation.html").write_text(template(other),encoding="utf-8")
    isolated.reload();isolated.wait_for_selector("#project-title")
    isolated.locator("#scratch-toggle").click()
    assert isolated.locator("#draft").input_value()==""
    isolated.locator("#draft").fill("project B")
    assert isolated.evaluate("localStorage.getItem('project-workboard:v2:"+data["meta"]["storageKey"]+":draft')")=="project A"
    assert isolated.evaluate("localStorage.getItem('legacy-workboard-draft')")=="preserve me"
    ok("project-specific drafts are isolated and legacy keys remain untouched")
    empty=json.loads(json.dumps(data));empty.pop("taskGroups",None);empty["tasks"]=[];empty["meta"].pop("currentTaskId",None)
    emptyPage=load(empty,name="empty")
    assert emptyPage.locator('[data-node="project"]').count()==1
    assert emptyPage.locator("#focus-current").is_disabled()
    ok("empty task set stays usable without inventing a current task")
    long=json.loads(json.dumps(data));long.pop("taskGroups",None);long["tasks"]=[{"id":"many","stage":"prepare","title":"Many siblings","status":"todo"}]
    long["tasks"] += [{"id":"item"+str(n),"stage":"prepare","parent":"many","title":"Item "+str(n),"status":"todo"} for n in range(80)]
    long["meta"]["currentTaskId"]="many"
    many=load(long,name="many");go(many,"task:many");many.locator('[data-toggle="task:many"]').click()
    assert many.locator('[data-node^="task:item"]').count()==80
    assert many.locator('#detail [data-go^="task:item"]').count()==80
    many.locator("#fit").click()
    r=many.locator("#canvas").bounding_box()
    boxes=many.locator("[data-node]").evaluate_all("(els)=>els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom}})")
    assert all(q["x"]>=r["x"]-1 and q["y"]>=r["y"]-1 and q["right"]<=r["x"]+r["width"]+1 and q["bottom"]<=r["y"]+r["height"]+1 for q in boxes)
    ok("long child lists expose every sibling and fit includes all visible nodes")
    textboard=json.loads(json.dumps(data));textboard.pop("taskGroups",None);textboard["tasks"]=[]
    textboard["stages"][0]["id"]="very_long_stage_"*20
    textboard["stages"][0]["state"]="Detailed sign-off explanation "*80
    textboard["meta"].pop("currentTaskId",None)
    textpage=load(textboard,name="long-text");textpage.locator("#overview").click();textpage.locator("#fit").click()
    assert textpage.locator(".node").evaluate_all("(nodes)=>nodes.every(node=>[...node.querySelectorAll('.node-id,.node-meta')].every(el=>{const a=el.getBoundingClientRect(),b=node.getBoundingClientRect();return a.right<=b.right+1&&a.bottom<=b.bottom+1}))")
    ok("long IDs and phase state summaries remain inside node boxes")
    if args.snapshot:
        source=Path(args.snapshot).read_text(encoding="utf-8")
        snap=json.loads(re.search(r'<script[^>]*type="application/json"[^>]*>([\s\S]*?)</script>',source)[1])
        snap["meta"]={"title":"Local scale test","storageKey":"local-scale-test","currentTaskId":"AMPC-32-03"}
        snap.setdefault("history",[]);snap.setdefault("sources",[]);snap.setdefault("decisions",[])
        large=load(snap,script=capture,name="large")
        go(large,"task:AMPC-32-03")
        toggle=large.locator('[data-toggle="task:AMPC-32-03"]')
        if toggle.get_attribute("aria-expanded")!="true":toggle.click()
        expected=[t["id"] for t in snap["tasks"] if t.get("parent")=="AMPC-32-03"]
        assert len(expected)==7
        for task in expected:assert large.locator('[data-node="task:'+task+'"]').count()==1
        go(large,"task:AMPC-32-03-07")
        assert "AMPC-32-03-07" in large.locator("#detail").inner_text()
        for parent in sorted({t.get("parent") for t in snap["tasks"] if t.get("parent")}):
            go(large,"task:"+parent)
            expected_children=[t["id"] for t in snap["tasks"] if t.get("parent")==parent]
            actual=large.locator("#detail [data-go]").evaluate_all("(els)=>els.filter(e=>e.closest('section').querySelector('h3')?.textContent.startsWith('直属子任务')).map(e=>e.dataset.go.slice(5))")
            assert actual==expected_children,parent
        assert large.evaluate("JSON.stringify(window.testBoard)===window.testBoardBefore")
        go(large,"task:AMPC-32-03-07")
        large.screenshot(path=str(artifacts/"large-local.png"),full_page=True)
        ok(str(len(snap["tasks"]))+"-task local snapshot: seven siblings visible immediately and deep task searchable")
    assert not errors,errors
    print(json.dumps({"passed":len(checks),"page_errors":errors,"artifacts":str(artifacts)},ensure_ascii=True),flush=True)
    context.close();browser.close()
