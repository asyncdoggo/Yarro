const sleep = (ms) => new Promise((res) => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
document.getElementById("u_image").setAttribute("src", `/images/${uname}`);
document.getElementById("profile-img").setAttribute("src", `/images/${uname}`);

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

document
    .getElementById("post_btn")
    .addEventListener("click", async function () {
        let cont = document.getElementById("postcontent").value;

        if (cont.trim().length > 0) {
            const response = await fetch("/api/newpost", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: cont }),
            }).then((response) => response.json());

            if (response.status == "success") {
                document.getElementById("postcontent").value = "";
                document.getElementsByTagName("post-section")[0].getPosts();
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

