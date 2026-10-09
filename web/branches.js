/* Accessible, local-only filter. Every branch remains in the rendered HTML with JS disabled. */
(function(){
  document.addEventListener("DOMContentLoaded",function(){
    const q=document.getElementById("branch-search");
    const type=document.getElementById("branch-category");
    const summary=document.getElementById("branch-visible");
    if(!q||!type||!summary)return;
    const rows=Array.from(document.querySelectorAll("[data-branch-row]"));
    function update(){
      const needle=q.value.trim().toLowerCase(),kind=type.value;
      let visible=0;
      rows.forEach(function(row){
        const okText=!needle||(row.dataset.search||"").includes(needle);
        const okType=!kind||row.dataset.category===kind;
        row.hidden=!(okText&&okType);
        if(!row.hidden)visible++;
      });
      summary.textContent=visible+" / "+rows.length+" branches";
    }
    q.addEventListener("input",update);
    type.addEventListener("change",update);
    update();
  });
})();
