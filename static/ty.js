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
const text = {
    change: (_node, _txt, _duration, include) => {
        let duration = _duration || 0.5;
        include && include.forEach(node => {
            let __node = document.querySelector(node);
            __node.style.transition = `opacity ${duration / 2}s linear`;
            __node.style.opacity = 0;
        });
        let node = document.querySelector(_node);
        node.style.transition = `opacity ${duration / 2}s linear`;
        node.style.opacity = 0;
        setTimeout(() => {
            include && include.forEach(node => document.querySelector(node).style.opacity = 1);
            node.innerHTML = _txt;
            node.style.opacity = 1;
        }, (duration * 1000) / 2);
        setTimeout(() => {
            include && include.forEach(node => document.querySelector(node).style.transition = `initial`);
            node.style.transition = `initial`;
        }, duration * 1000);
    },
};
const tyc = () => {
    text.change("section>main>div>h1>span", ty[Math.floor(Math.random() * ty.length)], null, ["section>main>div>h1"]);
    setTimeout(() => {
        tyc();
    }, 5000);
};
window.addEventListener("load", e => {
    changeImage();
    tyc();
    text.change("section>main>div>h2", ph[Math.floor(Math.random() * ph.length)]);
});