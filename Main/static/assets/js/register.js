// =====================================================
// Invalid login form handling
// =====================================================

const register_form = document.getElementsByClassName("register-form")[0];
const inputs = register_form.getElementsByTagName("input");

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
