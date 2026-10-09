/* Copy an explicitly selected researcher's full text; NEVER executes migration. */
(function(){
  "use strict";
  document.addEventListener("DOMContentLoaded",function(){
    document.querySelectorAll("[data-copy-owner-prompt]").forEach(function(button){
      const target=document.getElementById(button.getAttribute("data-copy-owner-prompt"));
      const status=button.parentElement.querySelector("[data-copy-status]");
      if(!target)return;
      button.addEventListener("click",async function(){
        let copied=false;
        try{
          if(navigator.clipboard && window.isSecureContext){
            await navigator.clipboard.writeText(target.value);
            copied=true;
          }else{
            target.focus();target.select();
            copied=!!document.execCommand("copy");
          }
        }catch(_){copied=false}
        if(copied){
          button.textContent="Copied researcher handover";
          if(status)status.textContent="Copied. Paste it only in this researcher's own chat.";
        }else{
          target.focus();target.select();
          if(status)status.textContent="Browser copy unavailable. The prompt has been selected for manual copying.";
        }
      });
    });
  });
})();
