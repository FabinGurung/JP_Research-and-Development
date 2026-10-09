/* Progressive animation enhancement: CPU-light CSS only; no remote rendering library. */
(function(){
  "use strict";
  document.addEventListener("DOMContentLoaded",function(){
    const scene=document.querySelector("[data-winged-book]");
    if(!scene)return;
    const button=scene.querySelector("[data-motion-toggle]");
    const reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if(!button)return;
    let manualPause=false,visible=true;
    function sync(){
      const paused=manualPause||!visible||document.hidden||reduce;
      scene.classList.toggle("motion-paused",paused);
      button.setAttribute("aria-pressed",String(manualPause));
      button.textContent=reduce?"Reduced motion active":manualPause?"Resume motion":"Pause motion";
      button.disabled=!!reduce;
      button.setAttribute("aria-label",reduce?"Animation disabled by your reduced-motion preference":manualPause?"Resume book animation":"Pause book animation");
    }
    button.addEventListener("click",function(){manualPause=!manualPause;sync()});
    document.addEventListener("visibilitychange",sync);
    if("IntersectionObserver" in window){
      const io=new IntersectionObserver(function(entries){visible=entries.some(x=>x.isIntersecting);sync()},{threshold:0.03});
      io.observe(scene);
    }
    sync();
  });
})();
