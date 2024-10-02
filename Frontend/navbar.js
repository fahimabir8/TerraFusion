fetch("navbar.html")
  .then((res) => res.text())
  .then((data) => {
    document.getElementById("navbar").innerHTML = data;

    const navElement = document.getElementById("user-section");
    const token = localStorage.getItem("token");

    if (token) {
      // Get the username from localStorage
      const username = localStorage.getItem("name");
      
      // Display the username and logout button in the navbar
      navElement.innerHTML = `
        <div class="flex items-center space-x-4">
          <span class="text-gray-900 dark:text-white font-medium">Hello, ${username}</span>
          <a id="logout" onclick="handleLogout()" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full font-semibold transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg">
            Logout
          </a>
        </div>
      `;

    } else {
      // If the user is not logged in, display the login/signup button
      navElement.innerHTML = `
        <a href="./registration_login.html" class="text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-full font-medium transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg">
          Login or Signup
        </a>
      `;
    }
  });