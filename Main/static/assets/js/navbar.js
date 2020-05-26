const navbar = document.getElementById("sticky_nav");

document.addEventListener("scroll", () => {
    
    if (window.scrollY > 1) {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    } else {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0)";
    }

});

const hideBtns = () => {

    if (window.screen.width < 750) {

        const nav_right = document.getElementById("sticky_nav").getElementsByClassName("nav-right")[0];
        const unlogged_btns = document.getElementById("sticky_nav").getElementsByClassName("unlogged");
        
    
        nav_right.style.marginRight = "-500px";
        setTimeout(() => {
            if (unlogged_btns) {
                for (const btn of unlogged_btns) {
                    btn.style.display = "none";
                }
            }
        }, 200);
    }

}

const showBtns = () => {

    if (window.screen.width < 750) {
        const nav_right = document.getElementById("sticky_nav").getElementsByClassName("nav-right")[0];
        const unlogged_btns = document.getElementById("sticky_nav").getElementsByClassName("unlogged");
        if (unlogged_btns) {
            for (const btn of unlogged_btns) {
                btn.removeAttribute("style");
            }
        }
        nav_right.removeAttribute("style");
    }

}