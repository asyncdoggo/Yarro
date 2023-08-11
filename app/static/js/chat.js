

let messages = {}


document.getElementById("profile-img").setAttribute("src",`/image/${localStorage.uid}`)

async function getUsers(params) {
        const response = await fetch(`/api/search?user=`, {
        method: 'GET',
    }).then((response) => response.json())

    let status = response.status;
    if (status == "success") {
        document.getElementById("chat_list").innerHTML = "";
        let data = response.data;
        if (data.length > 0) {
            for (let i in data) {
                document.getElementById("chat_list").innerHTML += `
                        <a href="#" onclick="setChat(this)" class="flex mt-2 items-center bg-white p-6 rounded-lg shadow group-data-[checked=true]:bg-black group-data-[checked=true]:shadow-gray-400" id="${data[i]['uid']}" name="${data[i]["username"]}">
                            <div class="flex-shrink-0">
                            <img class="h-12 w-12 rounded-full" src='/image/${data[i]["uid"]}' alt="User Avatar">
                            </div>
                            <div class="ml-6">
                            <h2 class="font-bold text-lg group-data-[checked=true]:text-white">${data[i]["name"]}</h2>
                            <p class="text-gray-700 group-data-[checked=true]:text-gray-500">@${data[i]["username"]}</p>
                            </div>
                        </a>
                    `

            }
        }
        else {
            document.getElementById("user_section").innerHTML = "No users found";

        }
    }
    else {
        Snackbar.show({ pos: "bottom-center", text: response.status })
    }
    
}


let token =  {}
let to_user_id = ""
let to_uname = ""

req = []

cookieStore.get("token").then(t => {
    token = t
})

getUsers()

function get_messages() {
    socket.emit("get_messages",{token:token.value,to_user:to_user_id,limit:10,page:0})
}


const socket = io("/")

document.getElementById("send").addEventListener("click", () =>{
    let msg = document.getElementById("msg").value
    socket.emit("send_message",{token:token.value,message:msg,to_user:to_user_id })
    document.getElementById("msg").value = ""
})


function setChat(e) {
    messages = {}
    while(x = req.pop()){
        clearInterval(x)
    }

    to_user_id = e.id
    to_uname = e.name
    x = setInterval(get_messages,500)
    req.push(x)
}


socket.on("messages", function(data,user_id,room){
    if (_.isEqual(data,messages)){
        return
    }
    messages = data.reverse()
    
    
    let msgs = document.getElementById("msg_list")
    msgs.innerHTML = ""

    for(i in messages){
        let msg = `
        
            ${
                messages[i].sender ? 
            `
                <div class="msg w-1/2 self-end" id="">
                <p class="self-start px-2">${localStorage.uname}</p>
                <p class="w-full border px-2 text-right rounded-full">${messages[i].content}</p>
            </div>
            `
                :
            `
            <div class="msg w-1/2 self-start" id="">
                <p class="self-start px-2">${to_uname}</p>
                <p class="w-full border px-2 text-right rounded-full">${messages[i].content}</p>
            </div>
`
            }
        `

        msgs.innerHTML += msg 
    }
})
