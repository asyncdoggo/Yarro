document.getElementById('reg_form').addEventListener('submit', async function (e) {
    document.getElementById("reg").disabled = true
    e.preventDefault();
    const form = new FormData(e.target);
    const senddata = Object.fromEntries(form.entries());
    // console.log(senddata["passwd1"])
    if (senddata["password"] == senddata["password2"]) {

        const response = await fetch("/api/login", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(senddata)
        }).then((response) => response.json())

        if (response.message == "success") {
            localStorage.setItem("uname", response.username);
            localStorage.setItem("uid", response.userId);
            window.location.href = "/"
        }
        else {
            Snackbar.show({ pos: "bottom-center", text: response.message })
            document.getElementById("reg").disabled = false
        }
    }
    else {
        Snackbar.show({ pos: "bottom-center", text: "passwords do not match" })
        document.getElementById("reg").disabled = false
    }
})
