let uname = window.location.pathname.split("/")[2]

document.getElementById("u_image").setAttribute("src", `/images/${uname}`);
document.getElementById("uname").innerHTML = uname


document.getElementById("homebtn").addEventListener("click", function () {
    window.location.href = "/"
})

document.getElementById("posts_section").innerHTML = `Login to see ${uname}'s posts`