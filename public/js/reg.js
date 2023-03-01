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
            localStorage.setItem("uid", response.uid)
            window.location.href = "/"
        }
        else {
            Snackbar.show({pos:"bottom-center",text: response.status})
            document.getElementById("reg").disabled = false
        }
    }
    else {
        Snackbar.show({pos:"bottom-center",text: "passwords do not match"})
        document.getElementById("reg").disabled = false
    }
})
