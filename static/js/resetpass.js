$(document).ready(function () {
    $("#resetButton").click(function () {

        let newpass1 = $("#newpass1").val();
        let newpass2 = $("#newpass2").val();
        let uname = $("#uname").text()

        if(newpass1 == newpass2){
            data = { "subject": "resetpass", "uname": uname,"pass1":newpass1}
            $.ajax({
                type: 'POST',
                url: "/",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: 'json',
                success: function (err, req, resp) {
                    msg = JSON.parse(resp["responseText"]);
                    if (msg["status"] == "success") {
                        $("#error").text("Reset successful");
                    }
                    else {
                        $("#error").text(msg["status"]);
                    }

                }
            })
        }
        else{
            $("#error").text("Passwords do not match")
        }
    })
})


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


