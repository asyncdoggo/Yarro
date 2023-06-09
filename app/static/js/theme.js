document.getElementById("parent").checked = true

let theme = localStorage.getItem("theme")
if (theme == "dark") {
    document.body.dataset.checked = true
    document.body.style.backgroundColor = "#101010"
    document.getElementById("theme_button").innerHTML = "light_mode"
    document.getElementById("theme").checked = true
}
else {
    document.body.dataset.checked = false
    document.body.style.backgroundColor = "#f7f7f7"
    document.getElementById("theme_button").innerHTML = "dark_mode"
}



document.getElementById("theme").addEventListener("change", (e) => {
    if (e.target.checked) {
        document.body.dataset.checked = true
        document.body.style.backgroundColor = "#101010"
        document.getElementById("theme_button").innerHTML = "light_mode"
        localStorage.setItem("theme", "dark")
    }
    else {
        document.body.dataset.checked = false
        document.body.style.backgroundColor = "#f7f7f7"
        document.getElementById("theme_button").innerHTML = "dark_mode"
        localStorage.setItem("theme", "light")
    }
})
