const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = localStorage.getItem("uname");

document.getElementById("username").innerHTML = uname
get_details()

document.getElementById("save_form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const response = await fetch("/api/updatedata", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }).then((response) => response.json())

    if (response.status = "success") {
        document.getElementById("errortext").innerHTML = "saved successfully"
    }

    const file = document.getElementById("image_upload").files[0]
    if (file != undefined) {

        var formdata = new FormData()
        formdata.append("image", file, uname)
        const response = await fetch("/api/sendimage", {
            method: 'POST',
            body: formdata
        }).then((response) => response.json())


    }
})

document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/"
})

document.getElementById("profile").addEventListener("click", function () {
    window.location.href = `/u/${uname}`
})

document.getElementById("logout").addEventListener("click", async function () {
    localStorage.clear()
    const response = await fetch("/api/logout", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
    if(response.status == "success"){
        window.location.reload()
    }
})



document.getElementById("image_upload").addEventListener("change", function () {
    const file = document.getElementById("image_upload").files[0]
    document.getElementById("user_image").setAttribute("src", URL.createObjectURL(file));
});


async function get_details() {
    const response = await fetch("/api/userdetails", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
    }).then((response) => response.json())

    if (response.status == "success") {
        res = response.data
        document.getElementById("user_image").setAttribute("src", `/images/${uname}`);
        document.getElementById("fname").value = res["fname"]
        document.getElementById("lname").value = res["lname"]
        document.getElementById("gender").value = res["gender"]
        document.getElementById("mob").value = res["mob"]
        document.getElementById("dob").value = res["dob"]
         document.getElementById("bio").value = res["bio"]


let str = document.getElementById("bio").value
document.getElementById("biocount").innerHTML = `Bio ${str.length}/255`
    }
}


document.getElementById("bio").addEventListener("input",function (e) {
    let str = document.getElementById("bio").value
    if(str.length > 255){
        str = str.substr(0,255)
        document.getElementById("bio").value = str
    }
    document.getElementById("biocount").innerHTML = `Bio ${str.length}/255`

})