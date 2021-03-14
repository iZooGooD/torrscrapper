document.querySelector("#menu-bar").addEventListener("click",openMobileMenu);
document.querySelector("#close-menu").addEventListener("click",closeMobileMenu);
function openMobileMenu(){
    document.querySelector(".mobile-menu").style.opacity="1";
    document.querySelector(".mobile-menu").style.width="50%";
    document.querySelector("#close-menu").style.animationName="animate";
    document.querySelector("#close-menu").style.animationDuration="1s";
    document.querySelector("#menu-bar").style.display="none";
}
function closeMobileMenu(){
    document.querySelector(".mobile-menu").style.width="0";
    document.querySelector("#close-menu").style.animationName="";
    document.querySelector("#close-menu").style.animationDuration="";
    document.querySelector(".mobile-menu").style.opacity="0";
    document.querySelector("#menu-bar").style.display="block";
}