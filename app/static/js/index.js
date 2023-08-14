


document.getElementById("passwd").addEventListener("focusin", (e) => {
    document.getElementById("pass").style.outlineWidth = "2px"
})

document.getElementById("passwd").addEventListener("focusout", (e) => {
    document.getElementById("pass").style.outlineWidth = "0px"
})


document.getElementById("pw").addEventListener("change", (e) => {
    if (e.target.checked) {
        document.getElementById("vis").innerHTML = "visibility_off"
        document.getElementById("passwd").type = "text"
    }
    else {
        document.getElementById("vis").innerHTML = "visibility"
        document.getElementById("passwd").type = "password"
    }
})


