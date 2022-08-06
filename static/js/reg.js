$(document).ready(function () {
    $('#reg_form').on('submit', function (e) {
        e.preventDefault();
        var senddata = $("#reg_form").serializeJSON();

        senddata["subject"] = "register";

        if (senddata["passwd1"] == senddata["passwd2"]) {

            $.ajax({
                type: 'POST',
                url: "/",
                data: JSON.stringify(senddata),
                contentType: "application/json",
                dataType: 'json',
                success: function (err, req, resp) {
                    msg = JSON.parse(resp["responseText"]);
                    if (msg["status"] == "success") {
                        localStorage.setItem("key", msg["key"]);
                        localStorage.setItem("uname", msg["uname"])
                        send_form("/",{"subject":"gotoreg2","uname":msg["uname"],"key":msg["key"]})
                    }
                    else if (msg["status"] == "alreadyuser") {
                        $("#error").text("User already exists");
                    }
                    else if (msg["status"] == "alreadyemail") {
                        $("#error").text("Email already exists");
                    }
                    else if (msg["status"] == "faliure") {
                        $("#error").text("An unknown error occured");
                    }
                    else {
                        $("#error").text(msg["status"]);
                    }
                }
            });

        }
        else {
            $("#error").text("passwords do not match");
        }
    })
});

function send_form(action, params) {
    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', action);

    for (var key in params) {
        if (params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


