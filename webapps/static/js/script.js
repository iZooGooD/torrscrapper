document.querySelector("#menu-bar").addEventListener("click", () => {
    const mobileMenu = document.querySelector(".mobile-menu");
    mobileMenu.style.opacity = "1";
    mobileMenu.style.width = "50%";
    document.querySelector("#close-menu").style.animation = "animate 1s";
    document.querySelector("#menu-bar").style.display = "none";
});

document.querySelector("#close-menu").addEventListener("click", () => {
    const mobileMenu = document.querySelector(".mobile-menu");
    mobileMenu.style.width = "0";
    document.querySelector("#close-menu").style.animation = "";
    mobileMenu.style.opacity = "0";
    document.querySelector("#menu-bar").style.display = "block";
});
