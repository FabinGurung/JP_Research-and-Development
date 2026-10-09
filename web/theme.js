/* Living Research Library: preserve legacy dusk selection; day is a scholarly parchment. */
(function(){
  "use strict";
  const root=document.documentElement;
  root.classList.add("js-enabled");
  const KEY="jp-rd-palette-v1";
  let chosen="dawn";
  try { if(localStorage.getItem(KEY)==="dusk") chosen="dusk"; } catch(_) {}
  root.setAttribute("data-theme",chosen);
  function paint(btn) {
    const night=root.getAttribute("data-theme")==="dusk";
    btn.textContent=night ? "☼ Day library" : "☾ Night library";
    btn.setAttribute("aria-label",night ? "Use the light reading-room theme" : "Use the dark reading-room theme");
    btn.setAttribute("aria-pressed",night?"true":"false");
  }
  document.addEventListener("DOMContentLoaded",function(){
    const btn=document.querySelector("[data-theme-toggle]");
    if(!btn)return;
    paint(btn);
    btn.addEventListener("click",function(){
      const next=root.getAttribute("data-theme")==="dusk"?"dawn":"dusk";
      root.setAttribute("data-theme",next);
      try{localStorage.setItem(KEY,next)}catch(_){}
      paint(btn);
    });
  });
})();
