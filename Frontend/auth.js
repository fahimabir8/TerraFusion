const handleRegistration = (event) =>{
    event.preventDefault();
    const username = getValue("username");
    const first_name = getValue("first_name");
    const email = getValue("email");
    const password = getValue("password");
    const confirm_password = getValue("confirm_password");
    const info = ({
        username,
        first_name,
        email,
        password,
        confirm_password,
    })
    if (password == confirm_password) {
        
        if(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/.test(password)){
            document.getElementById("error").innerText="Check Your Email For Confirmation";
            fetch("http://127.0.0.1:8000/account/register/",{
                method: "POST",
                headers: {"content-type": "application/json"},
                body: JSON.stringify(info),
            })
            .then((res) => res.json())
            .then((data) => console.log(data));
            console.log(data);
        }
        else{
            document.getElementById("error").innerText= "Password must contain minimum eight characters, at least one uppercase letter, one lowercase letter and one number."
        }
    }
    else {
        document.getElementById("error").innerText = "**Passwords do not match**";
    }
    
}

const getValue = (id) =>{
    const value = document.getElementById(id).value;
    return value;
}

const handleLogin = (event) => {
    event.preventDefault();
    const username = getValue("login-username")
    const password = getValue("login-password")
    const ans = ({
        username, password
    })
    fetch("http://127.0.0.1:8000/account/login/",{
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(ans),
    })
    .then(res => res.json())
    .then((data) => {
        if (data.token){
        console.log(data);
        localStorage.setItem("token", data.token);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("name", username);
        window.location.href = "./index.html"  
    }
    else {
        console.log(username,password);
        document.getElementById("login-error").innerText = "**Invalid username or password**"
    }
    })
    .catch((error) => {
        console.error("fetching problem:", error);
        document.getElementById("login-error").innerText = "Sorry for you inconvinence. Please try again.";
    });    
}

const handleLogout = () => {
    const token = localStorage.getItem("token");
    console.log("Token:", token);
    fetch("http://127.0.0.1:8000/account/logout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`,
        },
    })
    .then((res) => {
        console.log("Response status:", res.status);
        if (res.ok) {

            localStorage.clear();
            window.location.href = "./index.html";
        } else {
            console.log("Logout failed:", res.statusText);
        }
    })
    .catch((error) => {
        console.log("Logout error:", error);
    });
}
