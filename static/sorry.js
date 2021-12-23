const changeImage = () => {
    let i = Math.round(Math.floor(Math.random()*images.length));
    let e = Math.round(Math.floor(Math.random()*images.length));
    if (document.querySelector(".image-1").getAttribute("switched") === "1") {
        document.querySelector(".image-1").style.opacity = 1;
        document.querySelector(".image-1").setAttribute("switched", "0");
        setTimeout(() => {
            document.querySelector(`.image-2`).style.background = `url(${images[e].url})`;
        }, 2000);
    } else if (!document.querySelector(`.image-1`).getAttribute("switched")) {
        document.querySelector(`.image-1`).style.background = `url(${images[i].url})`;
        document.querySelector(".image-1").setAttribute("switched", "0");
        document.querySelector(`.image-2`).style.background = `url(${images[e].url})`;
    } else {
        document.querySelector(".image-1").style.opacity = 0;
        document.querySelector(".image-1").setAttribute("switched", "1");
        setTimeout(() => {
            document.querySelector(`.image-1`).style.background = `url(${images[i].url})`;
        }, 2000);
    };
    setTimeout(() => {
        changeImage();
    }, 10000);
};
window.addEventListener("load", e => {
    changeImage();
});