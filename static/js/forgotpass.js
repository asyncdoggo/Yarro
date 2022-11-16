document.getElementById("resetButton").addEventListener("click",async function () {

    var email = document.getElementById("email").value;

    const response = await fetch("/api/resetrequest", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "email": email })
    }).then((response) => response.json())
    let status = response.status
    if(status == "success"){
        document.getElementById("error").innerHTML = "Email sent successfully"
    }
    else if(status == "noemail"){
        document.getElementById("error").innerHTML = "Email does not exists"
    }
    else{
        document.getElementById("error").innerHTML = status
    }
})

