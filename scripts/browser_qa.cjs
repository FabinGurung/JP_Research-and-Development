#!/usr/bin/env node
"use strict";
/* Real Chromium QA of generated, PUBLIC static portal. No Google Drive, APIs or mutation. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { spawn } = require("node:child_process");
const { chromium } = require("playwright");
const { AxeBuilder } = require("@axe-core/playwright");
const root = path.resolve(__dirname, "..");
const base = "http://127.0.0.1:8765/";
const out = path.join(root, "browser-qa-output");
fs.mkdirSync(out, {recursive:true});
const findings = [];
const failures = [];
function record(name, detail) { findings.push({name, ...detail});console.log("BROWSER_QA",name,JSON.stringify(detail)); }
async function check(name, task) {
 try { await task(); record(name, {status:"PASS"}); }
 catch(err) { failures.push({name, error:String(err&&err.stack||err)});record(name,{status:"FAIL",error:String(err&&err.message||err)}); }
}
function assertNoOverflow(page, description) {
 return page.evaluate(({description}) => {
  const full=document.documentElement.scrollWidth, viewport=window.innerWidth;
  if(full>viewport+2) throw Error(description+" horizontal overflow "+full+" > "+viewport);
 }, {description});
}
async function main() {
 const server=spawn("python3",["-m","http.server","8765","--bind","127.0.0.1","--directory","dist"],{cwd:root,stdio:"ignore"});
 let browser;
 try {
  for(let i=0;i<55;i++){
   try{ const response=await fetch(base); if(response.ok)break; }catch(_){}
   await new Promise(r=>setTimeout(r,100));
  }
  browser=await chromium.launch({headless:true});
  const desktop=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1,permissions:["clipboard-read","clipboard-write"]});
  const page=await desktop.newPage();
  const javascriptErrors=[];
  page.on("pageerror",e=>javascriptErrors.push(String(e)));
  await check("desktop_hero_and_screenshot",async()=>{
   await page.goto(base,{waitUntil:"networkidle"});
   await page.locator("[data-winged-book]").waitFor();
   assert.equal(await page.locator("[data-motion-toggle]").count(),1);
   assert.ok((await page.locator("h1").first().innerText()).includes("Where curiosity"));
   await assertNoOverflow(page,"desktop");
   await page.screenshot({path:path.join(out,"desktop-home.png"),fullPage:true,animations:"disabled"});
  });
  await check("desktop_pause_and_resume",async()=>{
   const btn=page.locator("[data-motion-toggle]");
   await btn.click();
   assert.equal(await btn.getAttribute("aria-pressed"),"true");
   assert.equal(await page.locator(".flying-book").evaluate(e=>getComputedStyle(e).animationPlayState),"paused");
   await btn.click();
   assert.equal(await btn.getAttribute("aria-pressed"),"false");
  });
  await check("day_night_switch",async()=>{
   const btn=page.locator("[data-theme-toggle]");
   await btn.click();
   assert.equal(await page.locator("html").getAttribute("data-theme"),"dusk");
   await page.screenshot({path:path.join(out,"desktop-dusk.png"),animations:"disabled"});
  });
  await check("keyboard_navigation",async()=>{
   await page.keyboard.press("Tab");
   const active=await page.evaluate(()=>({
    tag:document.activeElement?.tagName,
    visible:document.activeElement?getComputedStyle(document.activeElement).visibility:""
   }));
   assert.ok(["A","BUTTON","INPUT","SELECT","TEXTAREA"].includes(active.tag),JSON.stringify(active));
   assert.notEqual(active.visible,"hidden");
  });
  await check("owner_prompt_copy",async()=>{
   await page.goto(base+"owner-prompts/fabin-gurung/",{waitUntil:"networkidle"});
   const text=await page.locator("#owner-prompt-text").inputValue();
   assert.ok(text.length>4000);
   assert.ok(text.includes("RSH-001"));
   await page.locator("[data-copy-owner-prompt]").click();
   await page.waitForFunction(() => document.querySelector("[data-copy-status]")?.textContent?.startsWith("Copied."),null,{timeout:7000});
   assert.equal(await page.locator("[data-copy-status]").innerText(),"Copied. Paste it only in this researcher's own chat.");
   const clip=await page.evaluate(()=>navigator.clipboard.readText());
   assert.equal(clip,text);
   await page.screenshot({path:path.join(out,"desktop-owner-prompt.png"),fullPage:true,animations:"disabled"});
  });
  await check("researcher_routes_and_portal_navigation",async()=>{
   for(const route of ["start-here/","search/","researchers/","thesis-infrastructure/","owner-prompts/","branches/","controls/latex/","roadmap/","how-to/"]){
    const response=await page.goto(base+route,{waitUntil:"domcontentloaded"});
    assert.equal(response.status(),200,route);
    assert.ok(await page.locator("main").count(),route);
   }
  });
  await check("catalogue_search_and_filter",async()=>{
   await page.goto(base+"search/",{waitUntil:"networkidle"});
   await page.locator(".search-result").first().waitFor();
   await page.locator("#research-search").fill("Safal");
   await page.waitForFunction(() => Number(document.querySelectorAll(".search-result").length)>0);
   assert.ok((await page.locator("#search-summary").innerText()).includes("matching catalogue"));
   await page.locator("#research-category").selectOption("Researchers");
   await page.waitForFunction(() => {
     const all=[...document.querySelectorAll(".search-category")];
     return all.length>0 && all.every(x=>x.textContent==="Researchers");
   },null,{timeout:6000});
   const visible=await page.locator(".search-category").allInnerTexts();
   assert.ok(visible.length>0);
   assert.ok(visible.every(x=>x.toLowerCase()==="researchers"));
   await page.screenshot({path:path.join(out,"desktop-search.png"),fullPage:true,animations:"disabled"});
   await page.locator("#research-search").focus();
   await page.keyboard.press("Escape");
   assert.equal(await page.locator("#research-search").inputValue(),"");
  });
  await check("desktop_wcag_axe",async()=>{
   await page.goto(base,{waitUntil:"networkidle"});
   const results=await new AxeBuilder({page}).withTags(["wcag2a","wcag2aa","wcag21aa"]).analyze();
   const serious=results.violations.filter(v=>v.impact==="critical"||v.impact==="serious");
   fs.writeFileSync(path.join(out,"axe-desktop.json"),JSON.stringify(results.violations,null,2));
   if(serious.length)throw Error("WCAG serious/critical: "+serious.map(x=>x.id+"("+x.nodes.length+")").join(", "));
  });
  await check("search_page_wcag_axe",async()=>{
   await page.goto(base+"search/",{waitUntil:"networkidle"});
   const results=await new AxeBuilder({page}).withTags(["wcag2a","wcag2aa","wcag21aa"]).analyze();
   const serious=results.violations.filter(v=>v.impact==="critical"||v.impact==="serious");
   fs.writeFileSync(path.join(out,"axe-search.json"),JSON.stringify(results.violations,null,2));
   if(serious.length)throw Error("Serious search accessibility findings: "+serious.map(x=>x.id).join(","));
  });
  await desktop.close();

  const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});
  const mp=await mobile.newPage();
  mp.on("pageerror",e=>javascriptErrors.push(String(e)));
  await check("mobile_390px_navigation_and_screenshot",async()=>{
   await mp.goto(base,{waitUntil:"networkidle"});
   assert.ok(await mp.locator("nav a").count()>=6);
   await assertNoOverflow(mp,"mobile homepage");
   await mp.screenshot({path:path.join(out,"mobile-home.png"),fullPage:true,animations:"disabled"});
  });
  await check("mobile_menu_keyboard_accessibility",async()=>{
   await mp.goto(base,{waitUntil:"networkidle"});
   const toggle=mp.locator("[data-mobile-menu]");
   const nav=mp.locator("#site-nav-links");
   assert.ok(await toggle.isVisible());
   assert.equal(await nav.isHidden(),true);
   await toggle.click();
   assert.equal(await toggle.getAttribute("aria-expanded"),"true");
   assert.ok(await nav.isVisible());
   await mp.keyboard.press("Escape");
   assert.equal(await toggle.getAttribute("aria-expanded"),"false");
   assert.equal(await nav.isHidden(),true);
   assert.equal(await toggle.evaluate(el=>document.activeElement===el),true);
  });
  await check("mobile_owner_prompt_and_copy_control",async()=>{
   await mp.goto(base+"owner-prompts/safal-dawadi/",{waitUntil:"networkidle"});
   await assertNoOverflow(mp,"mobile prompt");
   assert.ok(await mp.locator("[data-copy-owner-prompt]").isVisible());
   await mp.screenshot({path:path.join(out,"mobile-owner-prompt.png"),fullPage:true,animations:"disabled"});
  });
  await check("mobile_search_no_horizontal_overflow",async()=>{
   await mp.goto(base+"search/",{waitUntil:"networkidle"});
   await mp.locator(".search-result").first().waitFor();
   await assertNoOverflow(mp,"mobile catalogue");
   await mp.screenshot({path:path.join(out,"mobile-search.png"),fullPage:true,animations:"disabled"});
  });
  await check("mobile_wcag_axe",async()=>{
   await mp.goto(base,{waitUntil:"networkidle"});
   const results=await new AxeBuilder({page:mp}).withTags(["wcag2a","wcag2aa","wcag21aa"]).analyze();
   const serious=results.violations.filter(v=>v.impact==="critical"||v.impact==="serious");
   fs.writeFileSync(path.join(out,"axe-mobile.json"),JSON.stringify(results.violations,null,2));
   if(serious.length)throw Error("WCAG serious/critical: "+serious.map(x=>x.id+"("+x.nodes.length+")").join(", "));
  });
  await mobile.close();
  const reduced=await browser.newContext({viewport:{width:390,height:844},reducedMotion:"reduce"});
  const rp=await reduced.newPage();
  await check("mobile_320px_navigation",async()=>{
   await rp.goto(base,{waitUntil:"networkidle"});
   await rp.setViewportSize({width:320,height:700});
   await assertNoOverflow(rp,"320px narrow mobile");
   assert.ok(await rp.locator("[data-mobile-menu]").isVisible());
   await rp.screenshot({path:path.join(out,"mobile-320.png"),fullPage:true,animations:"disabled"});
  });
  await check("reduced_motion_disables_animation",async()=>{
   await rp.goto(base,{waitUntil:"networkidle"});
   assert.equal(await rp.locator(".flying-book").evaluate(e=>getComputedStyle(e).animationName),"none");
   assert.equal(await rp.locator("[data-motion-toggle]").isDisabled(),true);
  });
  await reduced.close();
  await check("progressive_navigation_without_javascript",async()=>{
   const nojs=await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:false});
   const nojsPage=await nojs.newPage();
   await nojsPage.goto(base,{waitUntil:"domcontentloaded"});
   assert.ok(await nojsPage.locator("#site-nav-links").isVisible());
   await assertNoOverflow(nojsPage,"no-JavaScript mobile");
   await nojs.close();
  });
  await check("no_uncaught_javascript_errors",async()=>{assert.deepEqual(javascriptErrors,[])});
 }finally{
  if(browser)await browser.close();
  server.kill("SIGTERM");
  fs.writeFileSync(path.join(out,"results.json"),JSON.stringify({status:failures.length?"FAIL":"PASS",findings,failures},null,2));
 }
 if(failures.length){console.error("BROWSER_QA_FAIL",JSON.stringify(failures));process.exitCode=1}
 else console.log("BROWSER_QA_PASS",findings.length);
}
main().catch(e=>{console.error("BROWSER_QA_FATAL",e);process.exitCode=1});
