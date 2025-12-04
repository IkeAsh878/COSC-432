//NavBar Initialization

document.addEventListener("DOMContentLoaded", () => {

  if (document.querySelector(".navbar")) return;
document.addEventListener("DOMContentLoaded", function () {

  const navbar = document.createElement("nav");
  navbar.classList.add("navbar");
  navbar.setAttribute("role", "navigation");
  navbar.setAttribute("aria-label","Main navigation");

  const logo = document.createElement("div");
  logo.classList.add("navbar-logo");
  logo.textContent = "OCA";

  const navLinks = document.createElement("ul");
  navLinks.classList.add("navbar-links");

  const links = [
    {name: "Home", href: "#" },
    {name: "About", href: "#about" },
    {name: "Services", href: "#services" },
    {name: "Contact", href: "#Contact"},
  ];

  links.forEach(link =>{
    const li = document.createElement("li");
    const a = document.createElement("a");

    a.textContent = link.name;
    a.href = link.href;
    a.classList.add("navbar-link");

    li.appendChild(a);
    navLinks.appendChild(li);
  });

  const logo = document.createElement("h1");
  logo.textContent = "OCA"; 

  navbar.appendChild(logo);
  navbar.appendChild(logo);
  navbar.appendChild(navLinks);

  document.body.prepend(navbar);
});

//Chat Functions
function appendChatMessage(text, type ="oca"){
  const chatHistory = document.getElementById("ChatHistory");
  if (!chatHistory) return console.error("Chat History containter not found");

  const msg = document.createElement("p");
  msg.textContent = text;
  msg.classList.add(type === "oca" ? "oca-msg" : "user-msg");

  chatHistory.appendChild(msg);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessageToGPT(userText) {
  try{
    const response = await fetch ("http://127.0.0.1:8000/chat", {
      method: "POST",
      header: { "Content-Type": "application/json" },
      body: JSON.stringify({message: userText})
  });

  if (!response.ok){
    throw new Error(`Server responded with ${response.status}`);
  }
  const data = await response.json();

  const reply = data?.reply ?? "[No reply from server]";

  appendChatMessage("OCA: " + reply, "oca"); 
  return reply;

  } catch (error){
    console.error("Error sending message:", error);
    appendChatMessage("OCA: Sorry something went wrong.", "oca");
    return null
  }
}
