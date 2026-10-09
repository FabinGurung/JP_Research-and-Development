/* Rose dawn is the default; dusk is user-selectable. Historical standalone demos are untouched. */
(function(){
  const KEY="jp-rd-palette-v1";
  const root=document.documentElement;
  let chosen="dawn";
  try { if(localStorage.getItem(KEY)==="dusk") chosen="dusk"; } catch(_) {}
  root.setAttribute("data-theme",chosen);
  function label(btn) {
    const isDusk=root.getAttribute("data-theme")==="dusk";
    btn.textContent=isDusk ? "☀ Dawn palette" : "☾ Dusk palette";
    btn.setAttribute("aria-label",isDusk?"Switch to rose dawn":"Switch to mauve dusk");
    btn.setAttribute("aria-pressed",isDusk?"true":"false");
  }
  document.addEventListener("DOMContentLoaded",function(){
    const btn=document.querySelector("[data-theme-toggle]");
    if(!btn) return;
    label(btn);
    btn.addEventListener("click",function(){
      const next=root.getAttribute("data-theme")==="dusk"?"dawn":"dusk";
      root.setAttribute("data-theme",next);
      try { localStorage.setItem(KEY,next); } catch(_) {}
      label(btn);
    });
  });
})();
