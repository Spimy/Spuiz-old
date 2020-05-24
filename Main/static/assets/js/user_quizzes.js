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

const showConfirmation = (quiz_title) => {
    event.preventDefault();
    const delete_confirmation = document.getElementById("delete_confirmation");

    delete_confirmation.getElementsByTagName("h1")[0].innerHTML = `Are you sure you want to delete "${quiz_title}"?`;
    delete_confirmation.style.transform = "scale(1)";
    delete_confirmation.style.backgroundColor = "rgba(var(--grey-dark-rgb), 0.8)";
}

const closeConfirmation = () => {
    event.preventDefault();
    const delete_confirmation = document.getElementById("delete_confirmation");
    delete_confirmation.removeAttribute("style");
}

const deleteQuiz = () => {

    const token = document.getElementsByTagName("input")[0].value;
    const data = new FormData();
    data.append("token", token);

    fetch(`${window.location.href}${selected_quiz}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": data.get("csrfmiddlewaretoken"),
            "X-Requested-With": "XMLHttpRequest"
        },
        body: data
    }).then(async res => {
        if (res.status === 200) {
            location.reload();
        }
    });

}