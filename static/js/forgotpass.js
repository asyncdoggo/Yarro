document
    .getElementById("resetButton")
    .addEventListener("click", async function () {
        document.getElementById("resetButton").disabled = true;
        var email = document.getElementById("email").value;
        try {
            const response = await fetch("/api/reset", {
                method: "PUT",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email: email }),
            }).then((response) => response.json());
            let status = response.status;
            if (status == "success") {
                Snackbar.show({
                    pos: "bottom-center",
                    text: "Email sent successfully",
                });
            } else if (status == "noemail") {
                Snackbar.show({
                    pos: "bottom-center",
                    text: "Email does not exists",
                });
            } else {
                Snackbar.show({
                    pos: "bottom-center",
                    text: status,
                });
            }
        } catch (error) {} 
        finally {
            document.getElementById("resetButton").disabled = false;
        }
    });
