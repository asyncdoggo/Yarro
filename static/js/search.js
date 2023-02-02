// var uname = localStorage.getItem("uname");

document.getElementById("searchForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    let user = document.getElementById("searchUsers").value;
    document.getElementById("user_section").innerHTML = "Loading";

    const response = await fetch(`/api/search?user=${user}`, {
        method: 'GET',
        }).then((response) => response.json())
    
        let status = response.status;
        if(status == "success"){
            document.getElementById("user_section").innerHTML = "";
            let data = response.data;
            if(data.length > 0){
                for(let i in data){
                    document.getElementById("user_section").innerHTML += `
                        <a href="/u/${data[i]['username']}" class="userCard flex flex-row shadow-md w-full pb-2 mb-2">
                        <div class="pfp-container max-w-[45px] min-w-[45px] min-h-[45px] pt-1 pr-4 mx-4">
                            <img src="/image/${data[i]['username']}" alt="pfp" class="min-w-[45px] h-[45px] rounded-full"/>
                        </div>
                        <div class="fullname-uname flex flex-col w-full">
                            <p class="text-lg font-medium">${data[i]["name"]}&nbsp;</p>
                            <p class="font-medium text-gray-500">@${data[i]['username']}</p>
                        </div>
                        </a>
                    `
                    history.pushState({},"",`/search?user=${user}`)

                }
            }
            else{
                document.getElementById("user_section").innerHTML = "No users found";

            }
        }
        else{
            Snackbar.show({pos:"bottom-center",text: response.status})
        }
    
        
});


document.getElementById("homebtn").addEventListener("click",function () {
    window.location.href = "/";
})