const login_form = document.getElementsByClassName("login-form")[0];
// =====================================================
// Invalid login form handling
// =====================================================

const inputs = login_form.getElementsByTagName("input");

for (const input of inputs) {

    if (input.name == "csrfmiddlewaretoken") continue;
    
    const field_label = input.parentElement.getElementsByTagName("label")[0];
    field_label.innerHTML += " <span class='required'>— field required</span>";

    input.addEventListener("invalid", event => {

        event.preventDefault();

        const required_msg = field_label.getElementsByTagName("span")[0];
        required_msg.classList.add("show");

        setTimeout(function() {
            required_msg.classList.remove("show");
        }, 10*1000);

    })

}

// =====================================================


// =====================================================
// AJAX for login form
// =====================================================

login_form.addEventListener("submit", event => {

    event.preventDefault();
    const data = new FormData(login_form);

    const xhr = new XMLHttpRequest()
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("X-CSRFToken", data.get("csrfmiddlewaretoken"));
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send(data);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status !== 200) {

                const msgs = document.getElementsByClassName("msgs")[0];
                msgs.innerHTML = JSON.parse(xhr.responseText)["msg"];
                messageEvent("msg-error", 10);

            } else {
                window.location = "/"
            }
        }  
    }

});

// =====================================================