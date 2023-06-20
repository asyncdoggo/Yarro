var uname = localStorage.getItem("uname");

document.getElementById("profile-img").setAttribute("src", `/image/${uname}`)

document.getElementById("searchForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    let user = document.getElementById("searchUsers").value;
    document.getElementById("user_section").innerHTML = "Loading";

    const response = await fetch(`/api/search?user=${user}`, {
        method: 'GET',
    }).then((response) => response.json())

    let status = response.status;
    if (status == "success") {
        document.getElementById("user_section").innerHTML = "";
        let data = response.data;
        if (data.length > 0) {
            for (let i in data) {
                document.getElementById("user_section").innerHTML += `
                        <a href="/u/${data[i]['username']}" class="flex mt-2 items-center bg-white p-6 rounded-lg shadow group-data-[checked=true]:bg-black group-data-[checked=true]:shadow-gray-400">
                          <div class="flex-shrink-0">
                            <img class="h-12 w-12 rounded-full" src='/image/${data[i]["uid"]}' alt="User Avatar">
                          </div>
                          <div class="ml-6">
                            <h2 class="font-bold text-lg group-data-[checked=true]:text-white">${data[i]["name"]}</h2>
                            <p class="text-gray-700 group-data-[checked=true]:text-gray-500">@${data[i]["username"]}</p>
                          </div>
                        </a>
                    `
                history.pushState({}, "", `/search?user=${user}`)

            }
        }
        else {
            document.getElementById("user_section").innerHTML = "No users found";

        }
    }
    else {
        Snackbar.show({ pos: "bottom-center", text: response.status })
    }


});


document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/";
})


document.getElementById("profile-btn").addEventListener("click", function () {
    window.location.href = `/u/${uname}`;
})


document
    .getElementById("logout-btn")
    .addEventListener("click", async function () {
        let x = localStorage.getItem("theme")
        localStorage.clear();
        localStorage.setItem("theme", x)

        const response = await fetch("/api/logout", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        }).then((response) => response.json());
        if (response.status == "success") {
            window.location.href = "/";
        }
    });
