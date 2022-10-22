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
    send_form("/profile", { "uname": uname, "token": token })
})

document.getElementById("logout").addEventListener("click", function () {
    localStorage.clear()
    send_form("/", { "subject":"logout","uname": uname, "token": token })
})

get_msg();


let pid;
let uid;
let content;
let lc;
let islike;
let date;

async function get_msg() {

    const response = await fetch("/api/posts", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ "self": "false" })
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
            islike = post["islike"];
            user = post["uname"];
            date = post["datetime"]
            var d = new Date(`${date} UTC`)
            d = d.toLocaleString("en-us");

            var like;
            if (islike) {
                like = `<span class="material-icons">thumb_up</span>`
            }
            else {
                like = `<span class="material-icons">
                            thumb_up_off_alt
                            </span>`
            }

            post = `<div class="post" id="${pid}">
                    <table class="main-table">
                        <tr>
                            <td class="profile_cell">
                                <div class="user_profile">
                                    <img src="/images/${user}" class="profile_img">
                                </div>
                            </td>
                            <td>
                                <table class="sub-table">
                                    <tr><p id="uname">${user}</p></tr>
                                    <tr><p id="content">${content}</p></tr>
                                    <tr>
                                        <div class="like_comment_buttons">
                                            <button id="${pid}" onClick=onButtonClick(this)>${like}</button>
                                            <p id="like_count">${lc}</p> &emsp;&emsp; <p>${d}</p>
                                        </div>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </div>
                <hr>`;

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

    const response = await fetch("/api/like", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ "pid": pid })
    }).then((response) => response.json())

    if(response.status == "success"){
        let like = document.getElementById(pid).getElementsByClassName("material-icons")[0]
        let lc = document.getElementById(pid).getElementsByTagName(`p`)[2]
        if(like.innerHTML.trim() == "thumb_up_off_alt"){
            like.innerHTML = "thumb_up"
            let temp = parseInt(lc.innerHTML)
            lc.innerHTML = ""
            lc.innerHTML = temp + 1
        }
        else{
            like.innerHTML = "thumb_up_off_alt"
            let temp = parseInt(lc.innerHTML)
            lc.innerHTML = ""
            lc.innerHTML = temp - 1
        }
    }
}