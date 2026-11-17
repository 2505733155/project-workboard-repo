const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const file=path.join(__dirname,'../project-workboard/assets/example/workboard-map.html');
let W={};
if(fs.existsSync(file)){
  const source=fs.readFileSync(file,'utf8').match(/<script id="workboard-engine">([\s\S]*?)<\/script>/)?.[1];
  if(source){const context=vm.createContext({URL});vm.runInContext(source,context);W=context.Workboard;}
}
const fixture=()=>({meta:{title:'Test',storageKey:'test',currentTaskId:'c2'},stages:[{id:'a',name:'A',state:'not accepted'},{id:'b',name:'B'}],tasks:[
{id:'p',stage:'a',parent:null,title:'Parent',status:'todo',deps:[]},
...['c1','c2','c3','c4','c5','c6','c7'].map(id=>({id,stage:'a',parent:'p',title:id,status:'todo',deps:[]})),
{id:'deep',stage:'a',parent:'c2',title:'Deep',status:'doing',deps:['c7']}
]});
const arr=x=>Array.from(x);
test('expansion exposes all seven direct children; selection never changes membership',()=>{
 const d=fixture(),before=JSON.stringify(d),i=W.build(d);
 assert.equal(i.errors.length,0);
 const want=['task:c1','task:c2','task:c3','task:c4','task:c5','task:c6','task:c7'];
 assert.deepEqual(arr(W.children(i,'task:p')),want);
 let expanded=new Set(['project','stage:a','task:p']);
 assert.deepEqual(arr(W.visible(i,expanded)).filter(k=>k.startsWith('task:')),['task:p',...want]);
 assert(!W.visible(i,expanded).includes('task:deep'));
 expanded=W.reveal(i,'task:deep',expanded);
 assert(W.visible(i,expanded).includes('task:deep'));
 assert.deepEqual(arr(W.children(i,'task:p')),want);
 expanded.delete('task:p');
 assert(!W.visible(i,expanded).includes('task:c1'));
 assert.equal(JSON.stringify(d),before);
});
test('deep hierarchy, arbitrary IDs and collision-safe namespaces',()=>{
 const d=fixture();d.tasks=[{id:'project',stage:'a',title:'Root ID',status:'todo'}];
 for(let n=0;n<40;n++)d.tasks.push({id:'x'+n,stage:'a',parent:n?'x'+(n-1):'project',title:'L'+n,status:'todo'});
 const i=W.build(d),expanded=W.reveal(i,'task:x39',new Set());
 assert.equal(i.errors.length,0);
 assert.equal(W.ancestors(i,'task:x39').length,43);
 const pos=W.layout(i,expanded);
 assert(pos.get('task:x39').x>pos.get('task:x38').x);
 assert.notEqual(pos.get('project'),pos.get('task:project'));
});
test('single stage and no tasks render as valid empty structures',()=>{
 const i=W.build({meta:{},stages:[{id:1,name:'One'}],tasks:[]});
 assert.equal(i.errors.length,0);
 assert.deepEqual(arr(W.visible(i,new Set(['project']))),['project','stage:1']);
 const empty=W.build({meta:{},stages:[],tasks:[]});
 assert.equal(empty.errors.length,0);assert.equal(W.layout(empty,new Set()).size,1);
});
test('siblings and variable depths have nonoverlapping boxes',()=>{
 const i=W.build(fixture()),p=W.layout(i,W.reveal(i,'task:deep',new Set(['project','stage:a','task:p'])));
 const boxes=arr(p.values());
 for(let a=0;a<boxes.length;a++)for(let b=a+1;b<boxes.length;b++){
 const x=boxes[a],y=boxes[b];
 assert(!(x.x<y.x+y.w&&x.x+x.w>y.x&&x.y<y.y+y.h&&x.y+x.h>y.y));
 }
});
test('duplicate, missing, cyclic and cross-stage parents are explicit errors',()=>{
 for(const change of [
 d=>d.tasks.push({...d.tasks[0]}),
 d=>d.tasks[0].parent='missing',
 d=>{d.tasks[0].parent='c1';},
 d=>{d.tasks[1].stage='b';},
 d=>{d.tasks[0].stage='missing';},
 d=>d.stages.push({...d.stages[0]}),
 d=>{d.tasks[0].parent='p';},
 d=>{d.tasks[0].status='not-a-state';},
 d=>{d.tasks[0].deps='c7';}
 ]){
 const d=fixture();change(d);const i=W.build(d);assert(i.errors.length>0,JSON.stringify(d));
 assert.doesNotThrow(()=>W.ancestors(i,'task:p'));
 }
});
test('dependency cycles and missing refs warn without becoming parent edges',()=>{
 const d=fixture();d.meta.currentTaskId='missing';d.tasks[0].deps=['c7','absent'];d.tasks[7].deps=['p'];
 const i=W.build(d);
 assert.equal(i.errors.length,0);assert(i.warnings.length>=3);
 assert.deepEqual(arr(W.children(i,'task:p')),['task:c1','task:c2','task:c3','task:c4','task:c5','task:c6','task:c7']);
});
test('wheel normalization handles pixel,line,page and Shift without double movement',()=>{
 const view={pan:{x:100,y:200},scale:1};
 let x=W.wheel(view,{deltaX:3,deltaY:5,deltaMode:0},{width:800,height:600});
 assert.equal(x.pan.x,97);assert.equal(x.pan.y,195);
 x=W.wheel(view,{deltaX:0,deltaY:2,deltaMode:1},{width:800,height:600});assert.equal(x.pan.y,168);
 x=W.wheel(view,{deltaX:1,deltaY:1,deltaMode:2},{width:800,height:600});assert.equal(x.pan.x,-700);assert.equal(x.pan.y,-400);
 x=W.wheel(view,{deltaX:6,deltaY:6,shiftKey:true},{width:800,height:600});assert.equal(x.pan.x,94);assert.equal(x.pan.y,200);
 assert.equal(view.pan.x,100);
});
test('Ctrl wheel preserves the world coordinate under the pointer',()=>{
 const view={pan:{x:20,y:30},scale:.8};
 const after=W.wheel(view,{deltaY:-50,ctrlKey:true,clientX:350,clientY:240},{left:50,top:40,width:800,height:600});
 assert(after.scale>.8);
 assert(Math.abs((300-20)/.8-(300-after.pan.x)/after.scale)<1e-9);
 assert(Math.abs((200-30)/.8-(200-after.pan.y)/after.scale)<1e-9);
});
test('stored view rejects corrupt data, removes stale IDs and bounds zoom',()=>{
 const i=W.build(fixture()),defaults={expanded:new Set(['project']),selected:'project',pan:{x:20,y:20},scale:.8};
 assert(W.restoreView('{broken',i,defaults).warning);
 const r=W.restoreView(JSON.stringify({expanded:['project','missing'],selected:'missing',pan:{x:4,y:8},scale:99}),i,defaults);
 assert.deepEqual(arr(r.view.expanded),['project']);assert.equal(r.view.selected,'project');assert(r.view.scale<=2);
 const bad=W.restoreView(JSON.stringify({pan:{x:'oops',y:0}}),i,defaults);assert(Number.isFinite(bad.view.pan.x));
});
test('evidence uses the configured root for root/nested boards and blocks active schemes',()=>{
 assert.equal(W.evidenceUrl('docs/a.md','./','file:///D:/project/board.html'),'file:///D:/project/docs/a.md');
 assert.equal(W.evidenceUrl('docs/a.md','../','file:///D:/project/views/board.html'),'file:///D:/project/docs/a.md');
 assert.equal(W.evidenceUrl('javascript:alert(1)','./','file:///D:/project/board.html'),null);
 assert.equal(W.evidenceUrl('data:text/html,bad','./','file:///D:/project/board.html'),null);
 assert.equal(W.evidenceUrl('C:\\notes\\a.md','./','file:///D:/project/board.html'),'file:///C:/notes/a.md');
});
test('explicit alternate state mapping drives semantic color without task rewriting',()=>{
 const d=fixture();d.statuses={backlog:{label:'Backlog',kind:'todo'}};d.tasks[0].status='backlog';
 const i=W.build(d);assert.equal(i.errors.length,0);
 assert.equal(i.statuses.get('backlog').color,'#465664');assert.equal(d.tasks[0].status,'backlog');
});
test('malformed reference types return actionable errors instead of throwing',()=>{
 for(const change of [
 d=>{d.tasks[1].parent={toString:null};},
 d=>{d.tasks[1].stage={toString:null};},
 d=>{d.tasks[1].deps=[{toString:null}];},
 d=>{d.meta.currentTaskId={toString:null};},
 d=>{d.tasks[0].status={toString:null};},
 d=>{d.statuses={alternate:{kind:{toString:null},label:'Alternate'}};},
 d=>{d.meta.title={toString:null};},
 d=>{d.tasks[0].description={toString:null};},
 d=>{d.stages[0].state={toString:null};},
 d=>{d.sources=[{label:{toString:null},path:'https://example.org/'}];},
 d=>{d.history=[{title:{toString:null},detail:'record'}];}
 ]){
 const d=fixture();change(d);let i;
 assert.doesNotThrow(()=>{i=W.build(d);});
 assert(i.errors.length>0);
 }
});

test('literal local evidence filenames preserve reserved characters while absolute URLs keep fragments',()=>{
 assert.equal(W.evidenceUrl('docs/review #1.pdf','./','file:///D:/project/board.html'),'file:///D:/project/docs/review%20%231.pdf');
 assert.equal(W.evidenceUrl('C:\\notes\\review #1.pdf','./','file:///D:/project/board.html'),'file:///C:/notes/review%20%231.pdf');
 assert.equal(W.evidenceUrl('review?.md','./','file:///D:/project/board.html'),'file:///D:/project/review%3F.md');
 assert.equal(W.evidenceUrl('https://example.org/report#section','./','file:///D:/project/board.html'),'https://example.org/report#section');
});

const grouped=()=>{
 const d=fixture();
 d.taskGroups=[
 {id:'first',parent:'p',stage:'a',title:'First category',taskIds:['c3','c1','c4'],description:'Explicit order'},
 {id:'second',parent:'p',stage:'a',title:'Second category',taskIds:['c2','c5','c6','c7'],tone:'doing'}
 ];
 return d;
};
test('explicit groups alter display paths without altering semantic parents or task totals',()=>{
 const d=grouped(),before=JSON.stringify(d),i=W.build(d);
 assert.equal(i.errors.length,0);
 assert.deepEqual(arr(W.children(i,'task:p')),['group:first','group:second']);
 assert.deepEqual(arr(W.children(i,'group:first')),['task:c3','task:c1','task:c4']);
 assert.deepEqual(arr(W.taskChildren(i,'task:p')),['task:c1','task:c2','task:c3','task:c4','task:c5','task:c6','task:c7']);
 assert.equal(i.taskParentMap.get('task:c2'),'task:p');
 assert.equal(i.parentMap.get('task:c2'),'group:second');
 assert.equal(arr(i.nodes.values()).filter(n=>n.type==='task').length,9);
 const ex=new Set(['project','stage:a','task:p']);
 assert.deepEqual(arr(W.visible(i,ex)).filter(id=>id.startsWith('group:')),['group:first','group:second']);
 assert(!W.visible(i,ex).includes('task:c3'));
 ex.add('group:first');
 assert(W.visible(i,ex).includes('task:c3'));
 assert(!W.visible(i,ex).includes('task:c2'));
 const revealed=W.reveal(i,'task:deep',ex);
 assert.deepEqual(arr(W.ancestors(i,'task:deep')),['project','stage:a','task:p','group:second','task:c2','task:deep']);
 assert(W.visible(i,revealed).includes('task:deep'));
 assert.deepEqual(arr(W.children(i,'task:p')),['group:first','group:second']);
 assert.equal(JSON.stringify(d),before);
 d.tasks[2].status='done';
 assert.deepEqual(arr(W.children(W.build(d),'group:second')),['task:c2','task:c5','task:c6','task:c7']);
});
test('eight and nine ungrouped tasks stay valid without automatic categories',()=>{
 for(const count of [8,9]){
 const d=fixture();d.tasks=[d.tasks[0],...Array.from({length:count},(_,n)=>({id:'m'+n,stage:'a',parent:'p',title:'Member',status:'todo'}))];
 const i=W.build(d);assert.equal(i.errors.length,0);
 assert.equal(W.children(i,'task:p').length,count);
 assert(!arr(i.nodes.values()).some(n=>n.type==='group'));
 }
});
test('group errors are actionable and never silently omit unassigned or duplicate members',()=>{
 for(const change of [
 d=>{d.taskGroups={};},
 d=>{d.taskGroups=[null];},
 d=>{d.taskGroups[0].id={toString:null};},
 d=>{d.taskGroups[0].parent={toString:null};},
 d=>{d.taskGroups[0].stage={toString:null};},
 d=>{d.taskGroups[0].taskIds=[{toString:null}];},
 d=>{d.taskGroups[0].title={toString:null};},
 d=>{d.taskGroups[0].tone='unmapped';},
 d=>{d.taskGroups[0].description={toString:null};},
 d=>{d.taskGroups[1].id='first';},
 d=>{d.taskGroups[1].taskIds.push('c3');},
 d=>{d.taskGroups[0].taskIds.push('c3');},
 d=>{d.taskGroups[0].taskIds.pop();},
 d=>{d.taskGroups[0].taskIds.push('missing');},
 d=>{d.taskGroups[0].taskIds.push('deep');},
 d=>{d.taskGroups[0].parent='missing';},
 d=>{d.taskGroups[0].stage='b';},
 d=>{d.taskGroups[0].parent='first';}
 ]){
 const d=grouped();change(d);let i;
 assert.doesNotThrow(()=>{i=W.build(d)});
 assert(i.errors.length>0,JSON.stringify(d.taskGroups));
 assert.equal(W.visible(i,new Set(['project','stage:a','task:p'])).length,0);
 }
});
test('nested grouping, empty categories and colliding business IDs remain navigable',()=>{
 const d=grouped();
 d.taskGroups[0].id='p';
 d.taskGroups.push({id:'empty',parent:'p',stage:'a',title:'Empty',taskIds:[]});
 d.taskGroups.push({id:'nested',parent:'c2',stage:'a',title:'Nested',taskIds:['deep']});
 d.tasks.find(t=>t.id==='deep').deps=['first'];
 const i=W.build(d);
 assert.equal(i.errors.length,0);assert(i.warnings.some(w=>w.includes('first')));
 assert.deepEqual(arr(W.children(i,'group:empty')),[]);
 assert.deepEqual(arr(W.ancestors(i,'task:deep')),['project','stage:a','task:p','group:second','task:c2','group:nested','task:deep']);
 assert(i.nodes.has('task:p')&&i.nodes.has('group:p'));
 const defaults={expanded:new Set(['project']),selected:'project',pan:{x:0,y:0},scale:1};
 const restored=W.restoreView(JSON.stringify({expanded:['project','group:gone'],selected:'group:gone',pan:{x:0,y:0},scale:1}),i,defaults);
 assert.equal(restored.view.selected,'project');assert(restored.warning);
});
