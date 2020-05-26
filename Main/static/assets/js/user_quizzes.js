// =====================================================
// Option selection
// =====================================================

const [completed_btn, created_btn] = document.getElementsByClassName("option-btn");
const [completed_card, created_card] = document.getElementsByClassName("card");

const option_btn_toggle = (remove_btn, add_btn, remove_card, add_card) => {
    if ([...add_btn.classList].includes("active")) return;

    remove_btn.classList.remove("active");
    add_btn.classList.add("active");

    remove_card.classList.remove("active");
    add_card.classList.add("active");
}

completed_btn.addEventListener("click", () => {
    option_btn_toggle(created_btn, completed_btn, created_card, completed_card);
});

created_btn.addEventListener("click", () => {
    option_btn_toggle(completed_btn, created_btn, completed_card, created_card);
});

// =====================================================


// =====================================================
// Handle follow/unfollow button
// =====================================================

const follow_unfollow_btn = document.getElementsByClassName("follow-unfollow")[0];

if (follow_unfollow_btn) {
    follow_unfollow_btn.addEventListener("click", event => {
    
        event.preventDefault();
        const token = document.getElementsByTagName("input")[0].value;
    
        fetch(follow_unfollow_btn.href, {
            method: "POST",
            headers: { "X-CSRFToken": token }
        }).then(async res => {
            
            if (res.status === 200) {
                
                res.json().then(value => {
                    const msgs = document.getElementsByClassName("msgs")[0];
    
                    const wrapper = document.createElement("div");
                    wrapper.innerHTML = value.new_page
                    const new_follow_unfollow_btn = wrapper.getElementsByClassName("follow-unfollow")[0]
    
                    follow_unfollow_btn.innerHTML = new_follow_unfollow_btn.innerHTML;
                    follow_unfollow_btn.setAttribute("href", new_follow_unfollow_btn.href);
                    msgs.innerHTML = value.msg;
                    messageEvent("msg-success", 3);
                });
    
            } else {
                const msgs = document.getElementsByClassName("msgs")[0];
                res.json().then(value => {
                    msgs.innerHTML = value.msg;
                    messageEvent("msg-error", 10);
                });
            }
    
        });
    
    });
}


// =====================================================


let selected_quiz;

const editPage = (page) => {
    event.preventDefault();
    window.location = page;
}

const showConfirmation = (event) => {
    event.preventDefault();
    const delete_confirmation = event.target.parentElement.parentElement.parentElement.getElementsByClassName("delete_confirmation")[0];
    const delete_card = delete_confirmation.getElementsByClassName("delete-card")[0];
    delete_confirmation.style.backgroundColor = "rgba(var(--grey-dark-rgb), 0.8)";
    delete_confirmation.style.zIndex = "5";
    delete_card.style.transform = "scale(1)";
}

const closeConfirmation = (btn) => {
    const delete_confirmation = btn.parentElement.parentElement.parentElement;
    const delete_card = delete_confirmation.getElementsByClassName("delete-card")[0];
    delete_confirmation.removeAttribute("style");
    delete_card.removeAttribute("style");
}

const deleteQuiz = (event) => {

    event.preventDefault();

    const token = document.getElementsByTagName("input")[0].value;
    const data = new FormData();
    data.append("csrfmiddlewaretoken", token);

    fetch(event.target.href, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": data.get("csrfmiddlewaretoken"),
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(async res => {
        if (res.status === 200) {
            location.reload();
        } else {
            const msgs = document.getElementsByClassName("msgs")[0];
            res.json().then(value => {
                msgs.innerHTML = value.msg;
                messageEvent("msg-error", 10);
            });
        }
    });

}