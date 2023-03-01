let e = true
document.getElementById("resend").addEventListener("click",async function(){
    if(e){
        const response = await fetch("/api/register", {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        }).then((response) => response.json())

        if(response.status == "success"){
            Snackbar.show({
                pos: "bottom-center",
                text: "email sent successfully",
            });
        }
    }
    e = false

    })
    