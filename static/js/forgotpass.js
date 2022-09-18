$(document).ready(function () {
    $("#resetButton").click(function () {

        var email = $("#email").val();

        data = { "subject": "forgotpass", "email": email }
        $.ajax({
            type: 'POST',
            url: "/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json',
            success: function (err, req, resp) {

                msg = JSON.parse(resp["responseText"]);


                if (msg["status"] == "success") {
                    $("#error").text("Email sent Successful");
                }
                else if (msg["status"] == "noemail") {
                    $("#error").text("Email does not exists");
                }
                else {
                    $("#error").text(msg["status"]);
                }

            }
        })
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


