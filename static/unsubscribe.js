const url = new URL(window.location.href);
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
    document.querySelector(`.yes`).addEventListener("click", f => {
        fetch(`/waitlist/remove_user?email=${url.searchParams.get("email")}&utk=${url.searchParams.get("utk")}`, {
            method: "DELETE"
        }).then(r=>r.json()).then(r => {
            if (r.success) {
                window.location.replace(`/waitlist/sorry?email=${url.searchParams.get("email")}&name=${r.name}&utm_from=unsubscribe`);        
            } else {
                window.location.replace(`/waitlist`);
            };
        });
    });
    document.querySelector(`.no`).addEventListener("click", f => {
        window.location.replace(`/waitlist/thanks?email=${url.searchParams.get("email")}&utm_from=unsubscribe`);
    });
});