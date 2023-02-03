const sleep = (ms) => new Promise((res) => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
let page = 0;
let bottom = false;
document.getElementById("u_image").setAttribute("src", `/image/${uname}`);
document.getElementById("profile-img").setAttribute("src", `/image/${uname}`);

document.getElementById("profile-btn").addEventListener("click", function () {
    window.location.href = `/u/${uname}`;
});

document.getElementById("cancle_btn").addEventListener("click", function () {
    document.getElementById("modal").hidden = true;
});

document.getElementById("postbox").addEventListener("click", function () {
    document.getElementById("modal").hidden = false;
    document.getElementById("postcontent").focus();
});

async function onBtnPress(pid, btn) {
    let islike = 0;
    if (btn.innerHTML.includes("thumb_up")) {
        islike = 1;
    }

    let buttons = btn.parentElement.parentElement;

    const response = await fetch("/api/like", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pid: pid, islike: islike }),
    }).then((response) => response.json());

    if (response.status == "success") {
        let data = response.data;
        if (data["islike"]) {
            buttons.children[0].children[0].innerHTML = "thumb_up";
        } else {
            buttons.children[0].children[0].innerHTML = "thumb_up_off_alt";
        }
        if (data["isdislike"]) {
            buttons.children[1].children[0].innerHTML = "thumb_down";
        } else {
            buttons.children[1].children[0].innerHTML = "thumb_down_off_alt";
        }

        buttons.children[0].children[1].innerHTML = data["lc"];
        buttons.children[1].children[1].innerHTML = data["dlc"];
    }
}

document.getElementById("post_btn")
        .addEventListener("click", async function () {
        let cont = document.getElementById("postcontent").value;

        if (cont.trim().length > 0) {
            const response = await fetch("/api/posts", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: cont }),
            }).then((response) => response.json());

            if (response.status == "success") {
                document.getElementById("postcontent").value = "";
                document.getElementById("post_section").innerHTML = "";
                page = 0;
                getPosts();
            }
        }
        document.getElementById("modal").hidden = true;
    });

document
    .getElementById("logout-btn")
    .addEventListener("click", async function () {
        localStorage.clear();
        const response = await fetch("/api/logout", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        }).then((response) => response.json());
        if (response.status == "success") {
            window.location.href = "/";
        }
    });


async function getPosts() {
    let response = await fetch(`/api/posts?page=${page}`, {
        method: "GET"
    }).then((response) => response.json());

    if (response.status == "success") {
        page += 10;
        let data = response.data;
        let keys = Object.keys(data).reverse();
        let i;
        const options = {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
        };
        
        let section = document.getElementById("post_section")
        
        for (i in keys) {
            var post = data[keys[i]];
            let pid = keys[i];
            let content = linkify(post["content"]);
            let lc = post["lc"];
            let dlc = post["dlc"];
            let islike = post["islike"];
            let isdislike = post["isdislike"];
            let user = post["uname"];
            let date = post["datetime"];
            let fullname = post["fullname"]
            let d = new Date(`${date} UTC`);
            d = d.toLocaleString("en-us", options);
            section.innerHTML += `<div class="post group flex flex-col shadow-md w-full pb-2 mb-2 " id="${pid}">
        <div class="first-row flex flex-row w-full">
            <div
                class="pfp-container max-w-[45px] min-w-[45px] min-h-[45px] pt-1 pr-4 mx-2"
            >
                <img src="/image/${user}" alt="pfp" class="min-w-[45px] h-[45px] rounded-full" />
            </div>
            <div class="fullname-date flex flex-col w-full">
                <div class="fullname mb-[-5px] flex flex-row w-full place-content-between">
                    <p class="text-lg font-medium ">${fullname}&nbsp;</p>
                    <div class="flex flex-row relative">
                        <p class="pr-8 text-xs ">${d}</p>
                    
                        ${uname != user ? "": `<div class="group/options flex flex-row">
                        <span class="material-icons right-0 hidden absolute hover:cursor-pointer group-hover:block">
                            keyboard_arrow_down
                        </span>
                        <div class="group-hover/options:block absolute hidden w-24 top-4 right-1 z-1 shadow-xl">
                            <p class="py-2 pl-2 hover:cursor-pointer bg-white hover:bg-gray-300" id="profile-btn" onClick=deleteRequest(${pid})>
                                Delete
                            </p>
                        </div>
                    </div>`}
                    </div>
                </div>
            <div class="username">
                <a href="/u/${user}" class="hover:underline underline-offset-1 accent-black font-medium text-gray-500 text-sm" >@${user}</a>
            </div>
            </div>
        </div>
        <div class="content pl-16 pr-2 whitespace-pre-wrap text-lg">${content}</div>
        <div class="buttons-row flex flex-row">
            <div class="lc flex flex-row pl-16 pt-4">
                <span class="material-icons w-full h-4 hover:cursor-pointer" onclick="onBtnPress(${pid},this)">${
                islike ? "thumb_up" : "thumb_up_off_alt"
            }</span>
                <p class="pl-2">${lc}</p>
            </div>
            <div class="dlc flex flex-row pl-4 pt-4">
                <span class="material-icons w-full h-4 hover:cursor-pointer" onclick="onBtnPress(${pid},this)">${
                isdislike ? "thumb_down" : "thumb_down_off_alt"
            }</span>
                <p class="pl-2">${dlc}</p>
            </div>
        </div>
    </div>`;
        }
    }
    bottom = false
}

function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 =
        /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(
        replacePattern1,
        '<a href="$1" target="_blank" class="underline underline-offset-1">$1</a>'
    );

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(
        replacePattern2,
        '$1<a href="http://$2" target="_blank" class="underline underline-offset-1">$2</a>'
    );

    //Change email addresses to mailto:: links.
    replacePattern3 =
        /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(
        replacePattern3,
        '<a href="mailto:$1" class="underline underline-offset-1">$1</a>'
    );

    return replacedText;
}


let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop
window.onscroll = function(ev) {
    var st = window.pageYOffset || document.documentElement.scrollTop;
    if (st > lastScrollTop && (window.innerHeight + window.scrollY) >= document.body.offsetHeight){
        getPosts()   
    }
    lastScrollTop = st <= 0 ? 0 : st;
};


async function deleteRequest(pid){
    const response = await fetch("/api/posts", {
        method: "DELETE",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pid: pid }),
    }).then((response) => response.json());
    if (response.status == "success") {
        page = 0
        document.getElementById(pid).remove();
    }
}


getPosts()