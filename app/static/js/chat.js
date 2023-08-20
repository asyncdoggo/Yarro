

let messages = {}

const user_id = localStorage.uid
document.getElementById("profile-img").setAttribute("src",`/image/${user_id}`)

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

                        <a onclick="setChat('${data[i]['uid']}','${data[i]['username']}')" id="${data[i]['uid']}"
                        class="flex items-center px-3 py-2 text-sm transition duration-150 ease-in-out border-b border-gray-300 cursor-pointer hover:bg-gray-300 focus:outline-none group-data-[checked=true]:hover:bg-gray-700">
                        <img class="object-cover w-10 h-10 rounded-full"
                        src='/image/${data[i]["uid"]}' alt="username" />
                        <div class="w-full pb-2">
                        <div class="flex justify-between">
                            <span class="block ml-2 font-semibold text-gray-600 group-data-[checked=true]:text-white">@${data[i]["username"]}</span>
                        </div>
                        <span class="block ml-2 text-sm text-gray-600 group-data-[checked=true]:text-white">${data[i]["name"]}</span>
                        </div>
                        <div>
                        <svg width="20" height="20" class="unread_svg" hidden>
                            <circle cx="8" cy="8" r="8" fill="green"></circle>
                        </svg>
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


let to_user_id = ""
let to_uname = ""

req = []


function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }
  
  const token =  getCookie("token")


const socket = io("/",{
    auth:{
        token: token
    }
})
  
  function get_messages() {
    socket.emit("get_messages",{token:token,to_user:to_user_id,limit:10,page:0})
}



document.getElementById("send").addEventListener("click", () =>{
    let msg = document.getElementById("msg").value
    if(msg.length >= 255){
        Snackbar.show({ pos: "bottom-center", text: "message should be less than 255 characters" })
        return
    }
    socket.emit("send_message",{token:token,message:msg,to_user:to_user_id })
    document.getElementById("msg").value = ""
})


function setChat(uid,uname) {
    document.getElementById("message_box").hidden = false
    document.getElementById(uid).getElementsByClassName("unread_svg")[0].setAttribute("hidden","")
    messages = {}
    document.getElementById("msg_list").innerHTML = `<div class="inline-block  h-8 w-8 animate-spin rounded-full border-4 border-solid border-current group-data-[checked=true]:text-white border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
    <span class="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">Loading...</span></div>`
    to_user_id = uid
    to_uname = uname
    document.getElementById("reciever_profile_img").setAttribute("src",`/image/${uid}`)
    document.getElementById("reciever_uname").innerText = uname
    
    get_messages()
}



socket.on("unread", function(data){
    for(i in data){
        document.getElementById(data[i]).getElementsByClassName("unread_svg")[0].removeAttribute("hidden")
    }
})


socket.on("messages", function(data){
    if(data["rec"] != to_user_id || data["uid"] != user_id) {
        document.getElementById(data["rec"]).getElementsByClassName("unread_svg")[0].removeAttribute("hidden")
        return
    }

    data = data["messages"]

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
            <div class="relative max-w-xl px-4 py-2 text-white bg-pink-400 rounded shadow">
              <span class="block">${messages[i].content}</span>
            </div>
          </li>
            `
            :
            `
            <li class="flex justify-start">
            <div class="relative max-w-xl px-4 py-2 text-gray-700 group-data-[checked=true]:bg-gray-700 group-data-[checked=true]:text-white rounded shadow">
              <span class="block">${messages[i].content}</span>
              </div>
          </li>
            `
        }
        `
        
        msgs.innerHTML += msg 
    }
})

getUsers()

socket.emit("get_unread",{token:token})