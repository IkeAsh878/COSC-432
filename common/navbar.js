document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.createElement("nav");
  navbar.classList.add("navbar");

  const logo = document.createElement("h1");
  logo.textContent = "OCA"; 
  navbar.appendChild(logo);

  document.body.insertBefore(navbar, document.body.firstChild);
});
