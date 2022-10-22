const sleep = ms => new Promise(res => setTimeout(res, ms));
let uname = localStorage.getItem("uname");
let token = localStorage.getItem("token");


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
            'x-access-tokens': token
        },
        body: JSON.stringify(data)
    }).then((response) => response.json())

    if(response.status = "success"){
        document.getElementById("errortext").innerHTML = "saved successfully"
    }

    const file = document.getElementById("image_upload").files[0]
    if (file != undefined) {

        var formdata = new FormData()
        formdata.append("image", file, uname)
        const response = await fetch("/api/sendimage", {
            method: 'POST',
            headers: {
                'x-access-tokens': token
            },
            body: formdata
        }).then((response) => response.json())
        
    
    }
})

document.getElementById("homebtn").addEventListener("click", function () {
    send_form("/", { "subject":"home", "token": token })
})

document.getElementById("logout").addEventListener("click", function (e) {
    e.preventDefault()
    localStorage.clear()
    send_form("/", { "subject":"logout", "token": token })
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
            'x-access-tokens': token
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
        // document.getElementById("age").value = res["age"]
    }
    else{
        window.location.href = "/"
    }
}

function send_form(action, params) {
    let form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', action);

    for (let key in params) {
        if (params.hasOwnProperty(key)) {
            let hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

