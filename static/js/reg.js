document.getElementById('reg_form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const senddata = Object.fromEntries(form.entries());

    if (senddata["passwd1"] == senddata["passwd2"]) {

        const response = await fetch("/api/register", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(senddata)
        }).then((response) => response.json())

        if (response.status == "success") {
            localStorage.setItem("token",response.token)
            localStorage.setItem("uname",senddata["uname"])
            send_form("/", { "subject": "home", "token":response.token})
        }
        else{
            document.getElementById("error").innerHTML = response.status
        }
    }
    else {
        document.getElementById("error").innerHTML = "passwords do not match";
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


