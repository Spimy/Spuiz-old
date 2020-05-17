const follow_unfollow_btn = document.getElementsByClassName("follow-unfollow")[0];

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