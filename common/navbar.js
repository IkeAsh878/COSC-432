//NavBar Initialization

document.addEventListener("DOMContentLoaded", () => {

  if (document.querySelector(".navbar")) return;

  const navbar = document.createElement("nav");
  navbar.classList.add("navbar");

  const logo = document.createElement("h1");
  logo.textContent = "OCA"; 

  navbar.appendChild(logo);
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
