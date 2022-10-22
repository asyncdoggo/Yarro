
let token = localStorage.getItem("token")


document.getElementById('reg2_form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const senddata = Object.fromEntries(form.entries());


    const response = await fetch("/api/updatedata", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-tokens': token

        },
        body: JSON.stringify(senddata)
    }).then((response) => response.json())


    console.log(response)

    if (response.status == "success") {
        send_form("/", { "subject": "home","token":token })
    }
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


