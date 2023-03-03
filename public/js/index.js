document.getElementById("login_form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const response = await fetch("/api/login", {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: data["uname"],
            password: data["passwd"]
        })
    }).then((response) => response.json())

    let status = response.message;
    if (status == "success") {
        localStorage.setItem("uname", response.username);
        localStorage.setItem("uid", response.userId);
        window.location.reload()
    }
    else {
        Snackbar.show({ pos: "bottom-center", text: response.status })
    }
})



