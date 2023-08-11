const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
let uid = localStorage.getItem("uid");

document.getElementById("profile-img").setAttribute("src", `/image/${uid}`);



document.getElementById("username").innerText = uname
get_details()

document.getElementById("save_form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const response = await fetch("/api/user_details", {
        method: 'PUT',
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then((response) => response.json())

    if (response.status = "success") {
        Snackbar.show({ pos: "bottom-center", text: response.status });
    }

    const file = document.getElementById("image_upload").files[0]
    if (file != undefined) {

        var formdata = new FormData()
        formdata.append("image", file, uname)
        const response = await fetch("/api/image", {
            method: 'POST',
            body: formdata
        }).then((response) => response.json())


    }
})

document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/"
})

document.getElementById("profile-btn").addEventListener("click", function () {
    window.location.href = `/u/${uname}`
})

document.getElementById("logout-btn").addEventListener("click", async function () {
    let x = localStorage.getItem("theme")
    localStorage.clear();
    localStorage.setItem("theme", x)

    const response = await fetch("/api/logout", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
    if (response.status == "success") {
        window.location.reload()
    }
})



document.getElementById("image_upload").addEventListener("change", function () {
    const file = document.getElementById("image_upload").files[0]
    document.getElementById("user_image").setAttribute("src", URL.createObjectURL(file));
});


async function get_details() {
    const response = await fetch("/api/user_details", {
        method: 'GET'
    }).then((response) => response.json())

    if (response.status == "success") {
        res = response.data
        document.getElementById("user_image").setAttribute("src", `/image/${uid}`);
        document.getElementById("name").value = res["name"]
        document.getElementById("gender").value = res["gender"]
        document.getElementById("mob").value = res["mob"]
        document.getElementById("dob").value = res["dob"]
        document.getElementById("bio").value = res["bio"]
    }
}