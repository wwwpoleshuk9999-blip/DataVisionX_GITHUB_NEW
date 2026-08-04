document.addEventListener("DOMContentLoaded",()=>{

    const box=document.getElementById("kpi-bar");
    if(!box) return;

    const observer=new MutationObserver(()=>{

        box.querySelectorAll(".kpi-item").forEach(card=>{

            card.classList.add("kpi-update");

            setTimeout(()=>{
                card.classList.remove("kpi-update");
            },400);

        });

    });

    observer.observe(box,{
        childList:true,
        subtree:true
    });

});
