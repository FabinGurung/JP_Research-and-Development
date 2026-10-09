/* Progressive mobile navigation; no JS leaves full link list available. */
(function(){
 "use strict";
 document.addEventListener("DOMContentLoaded",function(){
  const btn=document.querySelector("[data-mobile-menu]");
  const nav=document.getElementById("site-nav-links");
  if(!btn||!nav)return;
  function set(open){
   nav.classList.toggle("is-open",open);
   btn.setAttribute("aria-expanded",String(open));
   btn.textContent=open?"✕ Close menu":"☰ Menu";
  }
  btn.addEventListener("click",function(){set(btn.getAttribute("aria-expanded")!=="true")});
  nav.addEventListener("click",function(event){
   if(event.target.closest("a"))set(false);
  });
  document.addEventListener("keydown",function(event){
   if(event.key==="Escape"&&btn.getAttribute("aria-expanded")==="true"){set(false);btn.focus()}
  });
  const media=window.matchMedia("(min-width: 921px)");
  if(media.addEventListener)media.addEventListener("change",function(){set(false)});
  set(false);
 });
})();
