// =====================================================
// Media Quiz check box
// =====================================================

const media_quiz_checkbox = document.getElementById("media_quiz");
media_quiz_checkbox.addEventListener("change", () => {
    
    const questions = document.querySelectorAll(".questions-container > div");
    const questions_add_btn = document.querySelectorAll(".questions-container > div > input:nth-child(2)");

    for (let i=0; i<questions.length; i++) {
        if (media_quiz_checkbox.checked) {
            questions_add_btn[i].insertAdjacentHTML("afterend", `<div class="dropbox"><input type="file" class="question_thumbnail" accept="image/x-png,image/jpeg" onchange="showPreview(event)" required><p>Drop image here or click to upload</p><img style="display: none;" class="thumabnail-preview"></div><input type="button" onclick="clearPreview(this)" value="Reset Thumbnail" class="reset-thumbnail-btn">`);
        } else {
            questions[i].removeChild(questions[i].getElementsByClassName("dropbox")[0]);
            questions[i].removeChild(questions[i].getElementsByClassName("reset-thumbnail-btn")[0]);
        }
    } 

});

// =====================================================


let correct_answer_counter = 1;
let wrong_answer_counter = 1;

// =====================================================
// Answers
// =====================================================


const addAnswer = (type) => {

    if (type == "correct") {
        correct_answer_counter++;
    
        const div = document.createElement("div");
        div.innerHTML = `<input class="created" type="text" name="correct_answer_${correct_answer_counter}"  placeholder="..."> <input type="button" name="correct_position_${correct_answer_counter}" value="-" onclick="removeAnswer(this, '${type}')">`
        
        document.activeElement.parentElement.parentElement.parentElement.getElementsByClassName("correct-answers")[0].appendChild(div);
    } else if (type == "wrong") {
        wrong_answer_counter++;
    
        const div = document.createElement("div");
        div.innerHTML = `<input class="created" type="text" name="wrong_answer_${wrong_answer_counter}"  placeholder="..."> <input type="button" name="wrong_position_${wrong_answer_counter}" value="-" onclick="removeAnswer(this, '${type}')">`
        
        document.activeElement.parentElement.parentElement.parentElement.getElementsByClassName("wrong-answers")[0].appendChild(div);
    }

}
    
const removeAnswer = (div, type) => {
    if (type == "correct") {
        correct_answer_counter--;
    } else if (type == "wrong") {
        wrong_answer_counter--;
    }
    document.activeElement.parentElement.parentElement.parentElement.getElementsByClassName(`${type}-answers`)[0].removeChild(div.parentNode);
};

// =====================================================



// =====================================================
// Questions
// =====================================================

let question_counter = 1;

const questionString = (counter) => {
    return `
        <h3>Question</h3>
        <input type="text" name="question_${counter}" placeholder="..." required>
        <input type="button" name="question_position_${counter}" value="-" onclick=removeQuestion(this)>
        ${media_quiz_checkbox.checked ? `<div class="dropbox"><input type="file" class="question_thumbnail" accept="image/x-png,image/jpeg" onchange="showPreview(event)" required><p>Drop image here or click to upload</p><img style="display: none;" class="thumabnail-preview"></div><input type="button" onclick="clearPreview(this)" value="Reset Thumbnail" class="reset-thumbnail-btn">` : ''}
        <div>
            <div class="correct-answer-container">
                <h3>Correct Answers</h3>
                <div class="correct-answers">
                    <div>
                        <input type="text" name="correct_answer_${correct_answer_counter}" placeholder="..." required>
                        <input type="button" name="correct_position_${correct_answer_counter}" value="+" onclick="addAnswer('correct')">
                    </div>
                </div>
            </div>
            <div class="wrong-answer-container">
                <h3>Wrong Answers</h3>
                <div class="wrong-answers">
                    <div>
                        <input type="text" name="wrong_answer_${wrong_answer_counter}" placeholder="...">
                        <input type="button" name="wrong_position_${wrong_answer_counter}" value="+" onclick="addAnswer('wrong')">
                    </div>
                </div>
            </div>
        </div>
    `
}

const addQuestion = () => {
    question_counter++

    const div = document.createElement("div");
    div.className = "question-container";
    div.innerHTML = questionString(question_counter);

    document.getElementsByClassName("questions-container")[0].appendChild(div);
}

const removeQuestion = (div) => {
    document.getElementsByClassName("questions-container")[0].removeChild(div.parentNode);
}

// =====================================================

// =====================================================
// Create Quiz form submit
// =====================================================

const quiz_creator_form = document.getElementById("quiz-creator");
const mcq_checkbox = document.getElementById("mcq");
const msgs = document.getElementsByClassName("msgs")[0];

quiz_creator_form.addEventListener("submit", event => {
    event.preventDefault();

    const data = new FormData();
    const token = document.getElementsByTagName("input")[0].value;
    
    let question_counter = 0;
    const quiz_title = document.getElementById("quiz_title").value;
    const quiz_thumbnail = document.getElementById("quiz_thumbnail").files[0];
    const questions_list = document.getElementsByClassName("question-container");

    console.log(questions_list.length)

    const quiz = {
        "title": quiz_title,
        "media_quiz":  media_quiz_checkbox.checked,
        "mcq": mcq_checkbox.checked
    };
    
    const sorted_questions = [];
    
    for (const question_details of questions_list) {
        
        const correct = [];
        const wrong = [];

        const question = question_details.getElementsByTagName("input")[0].value;
        const correct_answers = question_details.querySelectorAll(".correct-answers > div");
        const wrong_answers = question_details.querySelectorAll(".wrong-answers > div");

        if (media_quiz_checkbox.checked) {
            question_counter++;
            const question_thumbnail = question_details.getElementsByClassName("question_thumbnail")[0].files[0];
            data.append(question_counter.toString(), question_thumbnail);
        }

        for (const correct_answer of correct_answers) {
            const answer = correct_answer.getElementsByTagName("input")[0].value;
            correct.push(answer);
            if (mcq_checkbox.checked) break;
        }

        if (mcq_checkbox.checked && wrong_answers.length < 3) {
            msgs.innerHTML = '<div id="msg-error">There must be at least 3 wrong answers for multiple choice questions quizzes!</div>';
            messageEvent("msg-error", 10);
            return;
        }
        
        let wrong_counter = 0;
        for (const wrong_answer of wrong_answers) {
            wrong_counter++;
            const answer = wrong_answer.getElementsByTagName("input")[0].value;

            if (mcq_checkbox.checked && answer == "") {
                msgs.innerHTML = '<div id="msg-error">There must be at least 3 wrong answers for multiple choice questions quizzes!</div>';
                messageEvent("msg-error", 10);
                return;
            }
            wrong.push(answer);
            if (mcq_checkbox.checked && wrong_counter == 3) break;
        }

        const question_object = {}
        question_object[question] = {
            "thumbnail": media_quiz_checkbox.checked ? question_counter.toString() : null,
            "correct": correct,
            "wrong": wrong
        }

        sorted_questions.push(question_object);
    }

    quiz["questions"] = sorted_questions;
    data.append("quiz", JSON.stringify(quiz));
    data.append("thumbnail", quiz_thumbnail);

    fetch(window.location.href, {
        method: "POST",
        headers: {
            "X-CSRFToken": token,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: data
    }).then(async res => {
        if (res.status === 200) {
            console.log("WORKED!")
            res.json().then(data => {
                window.location = data.quiz_url;
            });
        } else {
            res.json().then(data => {
                msgs.innerHTML = data.msg;
                messageEvent("msg-error", 10);
            });
        }
    });

});

// =====================================================



// =====================================================
// Image preview for thumbnails
// =====================================================

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
        const preview = event.target.parentElement.getElementsByClassName("thumabnail-preview")[0];

        preview.src = src;
        preview.style.display = "block";
        preview.style.cursor = "initial";
    }
}

const clearPreview = (btn) => {
    const preview = btn.parentElement.getElementsByClassName("thumabnail-preview")[0];
    preview.src = "";
    preview.style.display = "none";
    preview.parentElement.removeAttribute("style");
    preview.parentElement.getElementsByTagName("input")[0].value = "";
}

// =====================================================
