const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = window.location.pathname.split("/")[2]
document.getElementById("pfpimage").setAttribute("src", `/images/${uname}`);
document.getElementById("pfpimage2").setAttribute("src", `/images/${uname}`);

document.getElementById("uname").innerHTML = uname

try{
    document.getElementById("editprofile").addEventListener("click", function () {
        window.location.href = "/profile/edit"
    })
}catch(e){}

document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/"
})

document.getElementById("logout").addEventListener("click", async function () {
    localStorage.clear()
    const response = await fetch("/api/logout", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
    window.location.href = "/"
})

get_msg_bio_fullname();


const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: "numeric",
    minute: "numeric",
};

async function get_msg_bio_fullname() {

    let response = await fetch("/api/fullname", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"uname":uname})
    }).then((response) => response.json())

    if (response.status == "success") {
        let name = response.name
        let bio = response.bio
        document.getElementById("fullname").innerHTML = name
        document.getElementById("bio").innerHTML = bio
    }
}


function send_form(action, params) {
    let form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', action);

    for (let key in params) {
        if (params.hasOwnProperty(key)) {
            let hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


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
