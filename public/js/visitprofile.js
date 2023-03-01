let uname = window.location.pathname.split("/")[2]

document.getElementById("pfpimage").setAttribute("src", `/image/${uname}`);

document.getElementById("uname").innerHTML = uname


document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/"
})

document.getElementById("post_section").innerHTML = `Login to see ${uname}'s posts`