// =====================================================
// Check for viewport to change opacity and scale of question card
// =====================================================
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


// =====================================================
// AJAX
// =====================================================

const quiz_info_form = document.getElementsByClassName("quiz-info")[0];
const quiz_info_btns = quiz_info_form.getElementsByClassName("quiz-info-btns")[0];
const updownvote_btns = quiz_info_form.getElementsByClassName("quiz-updownvote");

quiz_info_form.addEventListener("submit", event => {

    event.preventDefault();

    const btn = document.activeElement;
    const token = quiz_info_form.getElementsByTagName("input")[0].value;
    const vote = btn.value;

    const data = new FormData();
    data.append("csrfmiddlewaretoken", token);
    data.append("vote", vote);
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("X-CSRFToken", token);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send(data);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {

                const wrapper = document.createElement("div");
                wrapper.innerHTML = JSON.parse(xhr.responseText)["updownvotebtns"];
                
                const quiz_info_btns_dom = wrapper.getElementsByClassName("quiz-info-btns")[0];
                quiz_info_btns.innerHTML = quiz_info_btns_dom.innerHTML;

            } else {

                const msgs = document.getElementsByClassName("msgs")[0];
                const wrapper = document.createElement("div");

                wrapper.innerHTML = JSON.parse(xhr.responseText)["msg"];
                msgs.innerHTML = wrapper.getElementsByClassName("msgs")[0].innerHTML
                messageEvent("msg-error", 10);

            }
        }  
    }

});

// =====================================================
