const sleep = ms => new Promise(res => setTimeout(res, ms));
let token = localStorage.getItem("token")
let uname = localStorage.getItem("uname")
document.getElementById("u_image").setAttribute("src", `/images/${uname}`);

document.getElementById("postbtn").addEventListener("click", async function () {

    let cont = document.getElementById("postcont").value


    const response = await fetch("/api/newpost", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ "content": cont })
    }).then((response) => response.json())

    if ((response.status) == "success") {
        document.getElementById("postcont").value = ""
        get_msg()
    }

});

document.getElementById("profile").addEventListener("click", function () {
    send_form('/profile')
})

document.getElementById("logout").addEventListener("click", function () {
    localStorage.clear()
    send_form("/", { "subject": "logout", "uname": uname, "token": token })
})

get_msg();

const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: "numeric",
    minute: "numeric",
};


let pid;
let uid;
let content;
let lc;
let dlc;
let islike;
let isdislike;
let date;

async function get_msg() {

    const response = await fetch("/api/posts", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ "latest":0 })
    }).then((response) => response.json())

    if (response.status == "success") {
        let data = response.data
        document.getElementById("post_section").innerHTML = "";
        for (i in Object.keys(data)) {
            var post = data[Object.keys(data)[i]]
            pid = Object.keys(data)[i];
            uid = post["uid"];
            content = post["content"];
            lc = post["lc"];
            dlc = post["dlc"]
            islike = post["islike"];
            isdislike = post["isdislike"]
            user = post["uname"];
            date = post["datetime"]
            var d = new Date(`${date} UTC`)
            d = d.toLocaleString("en-us", options);

            var like;
            var dislike;
            if (islike) {
                like = `<span class="material-icons" style="width:100%; height:10%; font-size:18px; border-radius:50%;">thumb_up</span>`
            }
            else {
                like = `<span class="material-icons" style="width:100%; height:10%; font-size:18px; border-radius:50%;">
                            thumb_up_off_alt
                            </span>`
            }

            if (isdislike) {
                dislike = '<span class="material-icons" style="width:100%; height:10%; font-size:18px; border-radius:50%">thumb_down</span>'
            }
            else {
                dislike = `<span class="material-icons" style="width:100%; height:10%; font-size:18px; border-radius:50%">
                            thumb_down_off_alt
                            </span>`
            }

            post = ` <div class="post" id="${pid}">
                    <div class="post-profile">
                        <div class="imager">
                        <img src="/images/${user}" class="profile_img">
                        </div>
                    </div>
                    <div class="post-content">
                        <div class="post-username" id="uname">
                            ${user}
                        </div>
                        <div class="post-time">
                            ${d}
                        </div>

                        <div class="post-message" id="content">
                            ${content}
                        </div>

                        <div class="post-info">
                            <div class="post-like">
                                <button id="${pid}" class="post-like-button" onClick=onButtonClick(this)>${like}</button>
                                <p id="like_count">${lc}</p>
                            </div>
                            <div class="post-dislike">
                                <button id="${pid}" class="post-dislike-button" onClick=onButtonClick(this)>${dislike}</button>
                                <p id="dislike_count">${dlc}</p>
                            </div>
                        </div>
                    </div>
                </div>`;

            document.getElementById("post_section").innerHTML += post;

        }
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


async function onButtonClick(btn) {
    let pid = btn.id
    let cname = btn.className
    let islike = 1;

    if (cname == "post-dislike-button") {
        islike = 0;
    }

    const response = await fetch("/api/like", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ "pid": pid,"islike":islike })
    }).then((response) => response.json())

    if (response.status == "success") {
        data = response.data
        let like = document.getElementById(pid).getElementsByClassName("material-icons")[0]
        let dislike = document.getElementById(pid).getElementsByClassName("material-icons")[1]
        let lc = document.getElementById(pid).getElementsByTagName(`p`).like_count
        let dlc = document.getElementById(pid).getElementsByTagName(`p`).dislike_count
        if(data["islike"] == 1){
            like.innerText = "thumb_up"
        }
        else{
            like.innerText = "thumb_up_off_alt"
        }
        if(data["isdislike"] == 1){
            dislike.innerText = "thumb_down"
        }
        else{
            dislike.innerText = "thumb_down_off_alt"
        }

        lc.innerHTML = data["lc"]
        dlc.innerHTML = data["dlc"]
    }
}