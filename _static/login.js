var passwordHash = "30368060324b67896ed46b75151f9c5293a3d10d"
var passwordCheck = false
var accessHomePagewhiteListConfig = ["http://127.0.0.1:8080/", "https://zengjf.fun/"]
var accessUriWhiteListConfig = [
    "src/0000_Template",
    "src/0013_Linux",
    "src/0001_RaspberryPi"
]

function submitUsernamePassword() {
    var username = document.getElementById("username").value
    var password = document.getElementById("password").value

    setLocalStorage("password", sha1(username + password))
    checkLogin(username, password)
}

function cleanUsernamePassword() {
    setLocalStorage("password", "")
}

function setLocalStorage(item, value){
    localStorage.setItem(item, value)
}

function getLocalStorage(item) {
    return localStorage.getItem(item)
}

function checkLogin(username, password) {
    if (getLocalStorage("password") != passwordHash) {
        alert("please check your:\nusername: " + username + "\npassword: " + password)
        window.location.href = "/login.html"
    } else {
        window.location.href = "/"
        console.log("password is ok")
    }
}

// console.log(window.location.href)
// console.log("password is: " + getLocalStorage("password"))

var accessUrl = window.location.href
var inWhiteList = false

if (passwordCheck) {
    if (!accessUrl.includes("login.html")) {

        for (i = 0; i < accessUriWhiteListConfig.length; i++) {
            if (accessUrl.includes(accessUriWhiteListConfig[i]))
                inWhiteList = true
        }

        for (i = 0; i < accessHomePagewhiteListConfig.length; i++) {
            if (accessUrl == accessHomePagewhiteListConfig[i])
                inWhiteList = true
        }

        if (!inWhiteList && getLocalStorage("password") != passwordHash) {
            window.location.href = "/login.html"
        } else {
            console.log("password is ok")
        }
    }
}
