var password = ""
var confirmPassword = ""
document.getElementById('passwd1').addEventListener('input', (event) => {
    password = event.target.value
    if (password.length == 0) event.target.style.borderColor = '#000000'
    else {
        event.target.style.borderColor = '#00ff00'
    }
})

document.getElementById('passwd2').addEventListener('input', (event) => {
    confirmPassword = event.target.value
    if (confirmPassword.length == 0) event.target.style.borderColor = '#000000'
    else {
        if (password == confirmPassword)
            event.target.style.borderColor = '#00ff00'
        else event.target.style.borderColor = '#ff0000'
    }
})

document.getElementById('reg_form').addEventListener('submit', async function (e) {
    document.getElementById("reg").disabled = true
    e.preventDefault();
    const form = new FormData(e.target);
    const senddata = Object.fromEntries(form.entries());
    // console.log(senddata["passwd1"])
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
            localStorage.setItem("uname", senddata["uname"])
            window.location.href = "/"
        }
        else {
            document.getElementById("error").innerHTML = response.status
            document.getElementById("reg").disabled = false
        }
    }
    else {
        document.getElementById("error").innerHTML = "passwords do not match";
        document.getElementById("reg").disabled = false
    }
})
