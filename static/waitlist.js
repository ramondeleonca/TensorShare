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
    for (el of document.querySelectorAll(`input[type="text"]`)) {
        el.addEventListener("focus", e => {
            document.querySelector(`label[for="${el.name}"]`).style.transform = "translate(0px, 0px) scale(0.75)";
        });
        el.addEventListener("focusout", e => {
            if (!el.value) document.querySelector(`label[for="${el.name}"]`).style.transform = "translate(5px, 35px)";
        });
    };
    for (eel of document.querySelectorAll(`input[type="email"]`)) {
        eel.addEventListener("focus", e => {
            document.querySelector(`label[for="${eel.name}"]`).style.transform = "translate(0px, 0px) scale(0.75)";
        });
        eel.addEventListener("focusout", e => {
            if (!eel.value) document.querySelector(`label[for="${eel.name}"]`).style.transform = "translate(5px, 35px)";
        });
    };
    // let df = document.querySelector(`#demo`);
    // df.addEventListener("change", e => {
    //     let nf = df.value.split("\\").at(-1);
    //     nf.normalize("NFC");
    //     let fn = nf.length>17?`${nf.slice(0, 16)}...${nf.split(".").at(-1)}`:nf;
    //     document.querySelector(`.fn`).innerHTML = `${fn||"Choose file"}`;
    //     document.querySelector(`.fn`).style.fontSize = "20px";
    // });
    document.querySelector(`.submit`).addEventListener("click", e => {
        let data = {
            name: document.querySelector(`#name`).value,
            email: document.querySelector(`#email`).value,
        };
        if (data.email && data.name) {
            e.preventDefault();
            signup(data.name, data.email);
        };
    });
});
const signup = (name, email) => {
    fetch(`${EP}/waitlist/add_user?email=${email}&name=${name}`, {
        method: "PUT",
    }).then(r=>r.json()).then(r => {
        if (r.success) {
            window.location.replace(`${EP}/waitlist/thanks?name=${name}&email=${email}&utm_from=waitlist_subscribe`);
        } else {
            window.location.replace(`${EP}/waitlist/thanks?name=${name}&email=${email}&utm_from=waitlist_subscribe&error=true&code=${r.code}`);
        };
    });
};