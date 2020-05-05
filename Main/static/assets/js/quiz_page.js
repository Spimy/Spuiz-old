// =====================================================
// Check for viewport to change opacity and scale of question card
const getElementsInArea = (function(docElm) {
    let viewportHeight = docElm.clientHeight;

    return function(e, opts){
        let found = [], i;
        
        if (e && e.type == "resize")
            viewportHeight = docElm.clientHeight;

        for (i = opts.elements.length; i--;){
            let elm        = opts.elements[i],
                pos        = elm.getBoundingClientRect(),
                topPerc    = pos.top / viewportHeight * 100,
                bottomPerc = pos.bottom / viewportHeight * 100,
                middle     = (topPerc + bottomPerc) / 2,
                inViewport = middle > opts.zone[1] && 
                             middle < (100-opts.zone[1]);

            elm.classList.toggle(opts.markedClass, inViewport);

            if (inViewport)
                found.push(elm);
        }
    };
})(document.documentElement);

window.addEventListener("scroll", f);
window.addEventListener("resize", f);

if (document.readyState !== "loading") {
    f();
} else {
    document.addEventListener("DOMContentLoaded", f);
}
  
if (document.addEventListener) document.addEventListener("DOMContentLoaded", f);

function f(e){
    getElementsInArea(e, {
        elements    : document.getElementsByClassName("question-card"), 
        markedClass : "highlight--1",
        zone        : [20, 20] // percentage distance from top & bottom
    });
    
    getElementsInArea(e, {
        elements    : document.getElementsByClassName("question-card"), 
        markedClass : "highlight--2",
        zone        : [40, 40] // percentage distance from top & bottom
    });
}
// =====================================================
