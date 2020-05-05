const navbar = document.getElementById("sticky_nav");

document.addEventListener("scroll", () => {
    
    if (window.scrollY > 1) {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0.6)";
    } else {
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0)";
    }

});