const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginiBtn = document.getElementById('login');

registerBtn.addEventListener('click', ()=>{
    container.classList.add("active");
})
loginiBtn.addEventListener('click', ()=>{
    container.classList.remove("active");
})

