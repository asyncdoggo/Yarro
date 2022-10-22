document.getElementById("resetButton").addEventListener("click",async function () {

    var email = document.getElementById("email").value;

    const response = await fetch("/api/resetrequest", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "email": email })
    }).then((response) => response.json())
    let status = response.status
    if(status == "success"){
        document.getElementById("error").innerHTML = "Email sent successfully"
    }
    else if(status == "noemail"){
        document.getElementById("error").innerHTML = "Email does not exists"
    }
    else{
        document.getElementById("error").innerHTML = status
    }
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


