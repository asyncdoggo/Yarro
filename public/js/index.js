document.getElementById("login_form").addEventListener("submit",async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

const response = await fetch("/api/login", {
    method: 'POST',
    headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
        "Authorization": "Basic " + btoa(data["uname"]+":"+data["passwd"])
    }
    }).then((response) => response.json())

    let status = response.status;
    if(status == "success"){
        localStorage.setItem("uname", response.uname);
        localStorage.setItem("uid", response.uid);
        window.location.reload()
    }
    else{
        Snackbar.show({pos:"bottom-center",text: response.status})
    }
})



