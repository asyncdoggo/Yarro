const uname = document.getElementById("uname").innerHTML

document.getElementById("resetButton").addEventListener("click", async function () {

    let newpass1 = document.getElementById("newpass1").value;
    let newpass2 = document.getElementById("newpass2").value;

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')
    const uid = urlParams.get('uid')


    if (newpass1 == newpass2) {

        const response = await fetch("/api/reset", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "uid": uid, "id": id, "pass1": newpass1 })
        }).then((response) => response.json())

        if (response.status) {
            window.location.href = "/"
        }
        else {
            document.getElementById("error").innerHTML = "Passwords do not match"
        }
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


