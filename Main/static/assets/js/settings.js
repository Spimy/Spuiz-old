const bio_form = document.getElementById("bio-form");
const save_btn = bio_form.getElementsByClassName("save-btn")[0];

const simplemde = new SimpleMDE({ 
    element: document.getElementById("bio"),
    initialValue: original_bio,
    hideIcons: ["fullscreen", "side-by-side", "guide"],
    showIcons: ["code"],
    promptURLs: true,
    spellChecker: false,
    tabSize: 4,
    status: ["lines", "words"]
});

simplemde.codemirror.on("change", () => {
    if (simplemde.value() != original_bio) {
        save_btn.style.display = "block";
    } else {
        save_btn.removeAttribute("style");
    }
});

const dropboxes = document.getElementsByClassName("dropbox");
for (const dropbox of dropboxes) {
    dropbox.addEventListener("dragover", () => {
        dropbox.style.color = "var(--purple-normal)";
        dropbox.style.outline = "2px dashed var(--purple-normal)";
    });
    dropbox.addEventListener("dragleave", () => {
        dropbox.removeAttribute("style");
    });
}


// =====================================================
// Option selection
// =====================================================

const [profile_btn, account_btn] = document.getElementsByClassName("option-btn");
const [profile_card, account_card] = document.getElementsByClassName("card");

const option_btn_toggle = (remove_btn, add_btn, remove_card, add_card) => {
    if ([...add_btn.classList].includes("active")) return;

    remove_btn.classList.remove("active");
    add_btn.classList.add("active");

    remove_card.classList.remove("active");
    add_card.classList.add("active");
}

profile_btn.addEventListener("click", () => {
    option_btn_toggle(account_btn, profile_btn, account_card, profile_card);
});

account_btn.addEventListener("click", () => {
    option_btn_toggle(profile_btn, account_btn, profile_card, account_card);
});

// =====================================================

// =====================================================
// AJAX for save button
// =====================================================

save_btn.addEventListener("click", event => {

    event.preventDefault();
    const token = bio_form.getElementsByTagName("input")[0].value;

    const data = new FormData();
    data.append("csrfmiddlewaretoken", token);
    data.append("bio", simplemde.value());


    fetch(window.location.href, {
        method: "POST",
        headers: {
            "X-CSRFToken": token,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: data
    }).then(async res => {
        if (res.status === 200) {
            res.json().then(data => {
                const msgs = document.getElementsByClassName("msgs")[0];
                msgs.innerHTML = data.msg;
                messageEvent("msg-success", 3);

                original_bio = simplemde.value();
                save_btn.removeAttribute("style");
            });
        }
    });

});

// =====================================================


// =====================================================
// AJAX for avatar and banner upload
// =====================================================

const ajaxUpload = (form_id, avatar=false) => {
    
    const form = document.getElementById(form_id);
    const input = form.getElementsByTagName("input")[1];
    const img = form.getElementsByTagName("img")[0]
    
    if (input.files.length > 0) {

        const dropbox = input.parentElement;
        
        dropbox.style.color = "var(--purple-normal)";
        dropbox.style.outline = "2px dashed var(--purple-normal)";
        
        const data = new FormData(form);
        
        fetch(window.location.href, {
            method: "POST",
            headers: {
                "X-CSRFToken": data.get("csrfmiddlewaretoken"),
                "X-Requested-With": "XMLHttpRequest"
            },
            body: data
        }).then(async res => {
            if (res.status === 200) {
                res.json().then(data => {
                    const msgs = document.getElementsByClassName("msgs")[0];
                    msgs.innerHTML = data.msg;
                    
                    const wrapper = document.createElement("div");
                    wrapper.innerHTML = data.settings;
                    
                    if (avatar) {
                        const navbar_avatar = document.querySelector(".avatar-container > img");
                        const navbar_avatar_dom = wrapper.querySelector(".avatar-container > img");
                        navbar_avatar.src = navbar_avatar_dom.src;
                    }
                    
                    const form_dom = wrapper.getElementsByClassName(form_id)[0];
                    const img_dom = form_dom.getElementsByTagName("img")[0];
                    img.src = img_dom.src;
                    
                    messageEvent("msg-success", 3);
                    dropbox.removeAttribute("style");
                });
            }
        });
    }
    
}

const avatar_form = document.getElementById("avatar-form");
const avatar_input = avatar_form.getElementsByTagName("input")[1];
avatar_input.addEventListener("change", () => { ajaxUpload("avatar-form", true) });

const banner_form = document.getElementById("banner-form");
const banner_input = banner_form.getElementsByTagName("input")[1];
banner_input.addEventListener("change", () => { ajaxUpload("banner-form") });
// =====================================================