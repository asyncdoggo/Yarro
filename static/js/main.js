const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
let key = localStorage.getItem("key");


$(document).ready(
    function () {

        $("#u_image").attr("src", `/images/${uname}`);


        $("#postbtn").click(function () {

            let cont = document.getElementById("postcont").value

            let msgdata = {
                "subject": "sendpost",
                "uname": uname,
                "key": key,
                "content": cont
            }

            $.ajax({
                type: 'POST',
                url: "/",
                data: JSON.stringify(msgdata),
                contentType: "application/json",
                dataType: 'json',
                success: function (err, req, resp) {
                    let res = JSON.parse(resp["responseText"]);
                    let status = res["status"];
                    if (status == "success") {
                        document.getElementById("postcont").value = ""
                    }
                }
            });
        });

        $("#profile").click(function () {
            send_form("/", { "subject": "profilepage", "uname": uname, "key": key })
        })

        $("#logout").click(function () {
            localStorage.setItem("uname", "")
            localStorage.setItem("key", "")
            send_form("/", { "subject": "logout", "uname": uname, "key": key })
        })

        document.querySelector("#homebtn").addEventListener("click", function () {
            send_form("/", { "subject": "mainpage", "uname": uname, "key": key })

        })



        get_msg();

    })

let pid;
let uid;
let content;
let lc;
let islike;



async function get_msg() {

    while (true) {
        let msgdata = {
            "subject": "getpost",
            "uname": uname,
            "key": key
        }

        $.ajax({
            type: 'POST',
            url: "/",
            data: JSON.stringify(msgdata),
            contentType: "application/json",
            dataType: 'json',
            success: function (err, req, resp) {
                let res = JSON.parse(resp["responseText"]);

                if (res["status"] == "success") {
                    let data = res["data"];
                    document.getElementById("post_section").innerHTML = "";
                    for (i in Object.keys(data)) {
                        var post = data[Object.keys(data)[i]]
                        pid = Object.keys(data)[i];
                        uid = post["uid"];
                        content = post["content"];
                        lc = post["lc"];
                        islike = post["islike"];
                        user = post["uname"];
                        var like;
                        if (islike) {
                            like = `<span class="material-icons">thumb_up</span>`
                        }
                        else {
                            like = `<span class="material-icons">
                            thumb_up_off_alt
                            </span>`
                        }

                        post = `
                                        <div class="post" id="${pid}">
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
                                            <p id="like_count">${lc}</p>
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
        });

        await sleep(1000);
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


function onButtonClick(btn) {
    let pid = btn.id

    let msgdata = {
        "subject": "updatelc",
        "key": key,
        "uname": uname,
        "pid": pid
    }

    $.ajax({
        type: 'POST',
        url: "/",
        data: JSON.stringify(msgdata),
        contentType: "application/json",
        dataType: 'json',
        success: function (err, req, resp) {
            let res = JSON.parse(resp["responseText"]);
            let status = res["status"]
        }
    });
    $
}