$(document).ready(function () {

    let uname = localStorage.getItem("uname")
    let key = localStorage.getItem("key")


    $('#reg2_form').on('submit', function (e) {
        e.preventDefault();
        var senddata = $("#reg2_form").serializeJSON();

        senddata["subject"] = "udetails";
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
                    console.log(msg)
                    send_form("/", { "subject": "mainpage", "uname": uname, "key": key})
                }
                else if (msg["status"] == "badkey") {
                    // send_form("/",{"subject":"keyerror"})
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


