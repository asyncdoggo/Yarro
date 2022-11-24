let e = true
document.getElementById("resend").addEventListener("click",async function(){
    if(e){
        const response = await fetch("/api/resend_confirm", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        }).then((response) => response.json())

        if(response.status == "success"){
            document.getElementById("error").innerHTML = "email sent successfully"
        }
    }

    e = false

    })
    