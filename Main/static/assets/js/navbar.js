const navbar = document.getElementById("sticky_nav");

document.addEventListener("scroll", () => {
    
    if (window.scrollY > 1) {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    } else {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0)";
    }

});

const hideBtns = () => {
    
    const unlogged_btns = document.getElementById("sticky_nav").getElementsByClassName("unlogged");
    
    if (unlogged_btns) {
        for (const btn of unlogged_btns) {
            btn.style.display = "none";
        }
    }


}

const showBtns = () => {

    const unlogged_btns = document.getElementById("sticky_nav").getElementsByClassName("unlogged");

    if (unlogged_btns) {
        for (const btn of unlogged_btns) {
            btn.removeAttribute("style");
        }
    }

}