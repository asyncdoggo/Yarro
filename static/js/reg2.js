$(document).ready(function () {
    $('#reg2_form').on('submit', function (e) {
        e.preventDefault();
        var senddata = $("#reg2_form").serializeJSON();

        senddata["subject"] = "reg2_data";
        senddata["key"] = localStorage.getItem("key")
        senddata["uname"] = localStorage.getItem("uname")

        $.ajax({
            type: 'POST',
            url: "/",
            data: JSON.stringify(senddata),
            contentType: "application/json",
            dataType: 'json',
            success: function (err, req, resp) {
                msg = JSON.parse(resp["responseText"]);
                if (msg["status"] == "success") {
                console.log("success");
                  // TODO GOTO MAINPAGE
                }
                else if (msg["status"] == "badkey") {
                send_form("/logout",{"subject":"keyerror"})
                }
                else {
                    $("#error").text(msg["status"]);
                }
            }
        });
    });
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


