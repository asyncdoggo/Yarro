let uname = localStorage.getItem("uname")

get_friends()


async function get_friends(){   
const response = await fetch("/api/get_friends", {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
}).then((response) => response.json())

let list = document.getElementById("friendlist")

if(response.status == "success"){
    let data = response.data
    for(i in data){
        let item = data[i]
        console.log(item)
        let user = item["user1"]
        
    if(user == uname){
        user = item["user2"]
    }

        list.innerHTML += `<label>${user}</label> <button>is friend</button><br>`
    }
}
}