const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
let key = localStorage.getItem("key");


$(document).ready(function () {



    let msgdata = {
        "subject": "getudetails",
        "uname": uname,
        "key": key
    }
    $("#username").val(uname)


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
                $("#user_image").attr("src", `/images/${uname}`);
                $("#fname").val(res["fname"])
                $("#lname").val(res["lname"])
                $("#gender").val(res["gender"])
                $("#mob").val(res["mob"])
                $("#dob").val(res["dob"])
                // document.getElementById("age").value = res["age"]
            }
        }
    });


    $("#save_form").on("submit", function (e) {
        e.preventDefault();
        var data = $("#save_form").serializeJSON();
        data["subject"] = "udetails";
        data["uname"] = uname;
        data["key"] = key;



        $.ajax({
            type: 'POST',
            url: "/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json',
            success: function (err, req, resp) {
                let res = JSON.parse(resp["responseText"]);
                $("#errortext").text("saved successfully")

            }
        });


        const file = document.getElementById("image_upload").files[0]
        if (file != undefined) {

            var formdata = new FormData()
            formdata.append("image", file, uname)
            formdata.append("uname",uname)
            formdata.append("key", true)

            $.ajax({
                type: "POST",
                url: "/sendimage",
                data: formdata,
                contentType: false,
                processData: false,
            })
        }
    })

    $("#logout").click(function () {
        localStorage.setItem("uname", "")
        localStorage.setItem("key", "")
        send_form("/", { "subject": "logout", "uname": uname, "key": key })
    })


});


document.getElementById("image_upload").addEventListener("change", function () {
    const file = document.getElementById("image_upload").files[0]
    $("#user_image").attr("src", URL.createObjectURL(file));
});


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

