/* Public static metadata search: browser local filtering, no analytics/network search APIs. */
(function(){
 "use strict";
 document.addEventListener("DOMContentLoaded",async function(){
  const input=document.getElementById("research-search");
  const category=document.getElementById("research-category");
  const results=document.getElementById("research-results");
  const summary=document.getElementById("search-summary");
  const more=document.getElementById("research-more");
  if(!input||!category||!results||!summary||!more)return;
  let entries=[],shown=24,filtered=[];
  function e(tag,cls,value){
   const el=document.createElement(tag);if(cls)el.className=cls;if(value!==undefined)el.textContent=value;return el;
  }
  function tokenize(value){return value.normalize("NFKD").toLocaleLowerCase().split(/\s+/).filter(Boolean)}
  function score(item,words){
   const title=item.title.toLocaleLowerCase(),body=(item.description+" "+item.keywords+" "+item.category).toLocaleLowerCase();
   if(!words.every(word=>title.includes(word)||body.includes(word)))return -1;
   return words.reduce((score,word)=>score+(title.startsWith(word)?7:title.includes(word)?4:1),0);
  }
  function append(item){
   const card=e("article","search-result");
   const header=e("div","search-meta");
   header.append(e("span","search-category",item.category));
   header.append(e("span","search-status",item.status));
   card.append(header);
   const link=e("a","search-title",item.title);
   link.href=item.url;
   if(/^https?:\/\//.test(item.url)){link.target="_blank";link.rel="noopener noreferrer"}
   card.append(link,e("p","",item.description));
   results.append(card);
  }
  function draw(){
   results.replaceChildren();
   filtered.slice(0,shown).forEach(append);
   more.hidden=filtered.length<=shown;
   summary.textContent=filtered.length+" matching catalogue records"+
       (filtered.length>shown?" · displaying first "+shown:"")+".";
   if(!filtered.length)results.append(e("p","muted","No matches. Try a researcher name, control tower, or Git branch."));
  }
  function update(){
   shown=24;
   const words=tokenize(input.value.trim());
   filtered=entries.filter(item=>!category.value||item.category===category.value)
      .map(item=>({item,rank:score(item,words)}))
      .filter(x=>x.rank>=0)
      .sort((a,b)=>b.rank-a.rank||a.item.title.localeCompare(b.item.title))
      .map(x=>x.item);
   draw();
   const params=new URLSearchParams();
   if(input.value.trim())params.set("q",input.value.trim());
   if(category.value)params.set("category",category.value);
   history.replaceState(null,"",location.pathname+(params.size?"?"+params:""));
  }
  more.addEventListener("click",function(){shown+=24;draw()});
  input.addEventListener("input",update);category.addEventListener("change",update);
  document.addEventListener("keydown",function(ev){
   if(ev.key==="/"&&!ev.ctrlKey&&!ev.metaKey&&!ev.altKey&&!["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)){ev.preventDefault();input.focus()}
   if(ev.key==="Escape"&&document.activeElement===input){input.value="";update();input.blur()}
  });
  try{
   const response=await fetch("../data/research-index.json",{cache:"no-store"});
   if(!response.ok)throw Error("HTTP "+response.status);
   const data=await response.json();entries=data.entries;
   [...new Set(entries.map(x=>x.category))].sort().forEach(x=>{const opt=e("option",null,x);opt.value=x;category.append(opt)});
   const url=new URL(location.href);
   input.value=url.searchParams.get("q")||"";
   const selected=url.searchParams.get("category")||"";
   if([...category.options].some(x=>x.value===selected))category.value=selected;
   update();
  }catch(error){
   summary.textContent="Catalogue could not load. Browse the researcher index instead.";
   results.append(e("p","muted","Source: data/research-index.json"));
  }
 });
})();
