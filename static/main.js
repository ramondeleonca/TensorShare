!function() {
    let dc = r.colData.split(":").at(-1).toString().split(",")
    let da = (parseInt(dc[0])+parseInt(dc[1])+parseInt(dc[2]))/3
    let di = r.dimen.split(",")
    document.querySelector(`#ds`).innerHTML = `
        :root {
            --c1: rgb(${r.colData.split(";")[0]});
            --c2: rgb(${r.colData.split(";")[1]});
            --c3: rgb(${r.colData.split(";")[2]});
            --c4: rgb(${r.colData.split(";")[3]});
            --domcol: rgb(${r.colData.split(":").at(-1)});
            --fcol: rgb(${da>127?"0,0,0":"255,255,255"});
            --scol: rgba(${da>127?"0,0,0":"255,255,255"},0.75);
        }
        .img {
            ${di[0]<di[1]?"height: auto":"width: auto"};
            ${di[0]<di[1]?"max-width: 90vw":"max-height: 85vh"};
            aspect-ratio: ${di[0]} / ${di[1]};
            border-radius: ${di[0]<di[1]?"2vh":"2vw"};
        }
        .inf-img {
            ${di[0]<di[1]?"height: auto":"width: auto"};
            ${di[0]<di[1]?"max-width: 30vw":"max-height: 75vh"};
            aspect-ratio: ${di[0]} / ${di[1]};
            border-radius: ${di[0]<di[1]?"2vh":"2vw"};
        }
    `.replace("\n", "").replace(" ", "");
    window.onload = e => {
        AOS.init();
        document.querySelector(`.bgo`).classList.add("active");
        window.onscroll = e => {
            document.querySelector(`.wrapper`).style.transform = `translateY(-${window.scrollY}px)`
        };
        document.querySelector(`.exif>ul>#model>p`).innerHTML = `Model: ${r.exif.Model||"Unknown"}`;
        document.querySelector(`.exif>ul>#software>p`).innerHTML = `Software: ${r.exif.Software||"Unknown"}`;
        document.querySelector(`.exif>ul>#date>p`).innerHTML = `Date: ${r.exif.DateTime?r.exif.DateTime.split(" ")[0].replace(":", "/"):"Unknown"} at ${r.exif.DateTime?r.exif.DateTime.split(" ")[1]:"Unknown time"}`;
        document.querySelector(`.exif>ul>#maker>p`).innerHTML = `Maker: ${r.exif.Maker||"Unknown"}`;
        document.querySelector(`.exif>ul>#iat>p`).innerHTML = `Issued at ${r.iat}`;
    };
}();