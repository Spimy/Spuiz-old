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

const showPreview = (event) => {
    if (event.target.files.length > 0) {
        const src = URL.createObjectURL(event.target.files[0]);
        const preview = document.getElementsByClassName("thumabnail-preview")[0];

        preview.src = src;
        preview.style.display = "block";
        preview.style.cursor = "initial";
    }
}

const edit_quiz_form = document.getElementsByClassName("card")[0];

const submitForm = (event) => {
    event.preventDefault();

    const data = new FormData(edit_quiz_form);

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
                console.log(data.quiz_url)
                window.location = data.quiz_url;
            });
        }
    });

}