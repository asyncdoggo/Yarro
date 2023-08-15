

document.getElementById("login_form").addEventListener("submit", async function (e) {
    document.getElementById("login_btn").disabled = true
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const response = await fetch("/api/login", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": "Basic " + btoa(data["uname"] + ":" + data["passwd"])
        }
    }).then((response) => response.json())

    let status = response.status;
    if (status == "success") {
        localStorage.setItem("uname", response.uname);
        localStorage.setItem("uid", response.uid);
        window.location.reload()
    }
    else {
        Snackbar.show({ pos: "bottom-center", text: response.status })
    }
    document.getElementById("login_btn").disabled = false

})


document.getElementById("passwd").addEventListener("focusin", (e) => {
    document.getElementById("pass").style.outlineWidth = "2px"
})

document.getElementById("passwd").addEventListener("focusout", (e) => {
    document.getElementById("pass").style.outlineWidth = "0px"
})


document.getElementById("pw").addEventListener("change", (e) => {
    if (e.target.checked) {
        document.getElementById("vis").innerHTML = "visibility_off"
        document.getElementById("passwd").type = "text"
    }
    else {
        document.getElementById("vis").innerHTML = "visibility"
        document.getElementById("passwd").type = "password"
    }
})


