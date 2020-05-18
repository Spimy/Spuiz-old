// =====================================================
// AJAX for Upvotes and Downvotes
// =====================================================

const btns = document.getElementsByClassName("btns")[0];
const updownvote_btns = btns.getElementsByClassName("updownvote-btn");
const stars = document.getElementsByClassName("stars")[0];

btns.addEventListener("submit", event => {

    event.preventDefault();

    const btn = document.activeElement;
    const token = btns.getElementsByTagName("input")[0].value;
    const vote = btn.value;

    const data = new FormData();
    data.append("csrfmiddlewaretoken", token);
    data.append("vote", vote);
    data.append("from_complete", true);
    
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
                
                const btns_dom = wrapper.getElementsByClassName("btns")[0];
                const stars_dom = wrapper.getElementsByClassName("stars")[0];
                btns.innerHTML = btns_dom.innerHTML;
                stars.innerHTML = stars_dom.innerHTML;

            } else {

                const msgs = document.getElementsByClassName("msgs")[0];
                msgs.innerHTML = JSON.parse(xhr.responseText)["msg"];
                messageEvent("msg-error", 10);

            }
        }  
    }

});

// =====================================================
