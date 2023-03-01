document.getElementById("resetButton").addEventListener("click", async function () {

    let newpass1 = document.getElementById("newpass1").value;
    let newpass2 = document.getElementById("newpass2").value;

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')
    const uid = urlParams.get('uid')


    if (newpass1 == newpass2) {

        const response = await fetch("/api/reset", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "uid": uid, "id": id, "pass1": newpass1 })
        }).then((response) => response.json())

        if (response.status) {
            window.location.href = "/"
        }
        else {
            Snackbar.show({
                pos: "bottom-center",
                text: "Passwords do not match",
            });
        }
    }
})
