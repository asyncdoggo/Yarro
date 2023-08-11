

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

                        <a onclick="setChat('${data[i]['uid']}','${data[i]['username']}')"
                        class="flex items-center px-3 py-2 text-sm transition duration-150 ease-in-out border-b border-gray-300 cursor-pointer hover:bg-gray-100 focus:outline-none">
                        <img class="object-cover w-10 h-10 rounded-full"
                        src='/image/${data[i]["uid"]}' alt="username" />
                        <div class="w-full pb-2">
                        <div class="flex justify-between">
                            <span class="block ml-2 font-semibold text-gray-600">@${data[i]["username"]}</span>
                        </div>
                        <span class="block ml-2 text-sm text-gray-600">${data[i]["name"]}</span>
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


function setChat(uid,uname) {
    messages = {}
    while(x = req.pop()){
        clearInterval(x)
    }

    to_user_id = uid
    to_uname = uname
    document.getElementById("reciever_profile_img").setAttribute("src",`/image/${uid}`)
    document.getElementById("reciever_uname").innerText = uname

    x = setInterval(get_messages,100)
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
            <li class="flex justify-end">
            <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 rounded shadow">
              <span class="block">${messages[i].content}</span>
            </div>
          </li>
            `
                :
            `
            <li class="flex justify-start">
            <div class="relative max-w-xl px-4 py-2 text-gray-700 rounded shadow">
              <span class="block">${messages[i].content}</span>
            </div>
          </li>
            `
            }
        `

        msgs.innerHTML += msg 
    }
})
