


//ask for the current tab url
var url;
var nickname;
chrome.runtime.sendMessage({ action: 'getUrl' }, (response)=>{
}); //send request to service worker

//get response from serviceworker
chrome.runtime.onMessage.addListener ( function(message){
  url = message.vidID;
  nickname=  message.IGN;

  if(url!="xxxxxxxxxxx"){
    startConnection(nickname,url);
  }
  else
  {
    document.getElementById("chatBox").innerHTML="Sorry, extension only works for youtube. however suggestions are welcome."
    document.getElementById("nameSection").innerHTML = "<h2>Offline <br> Bad url.</h2>";

  }
});



var nickname;



function startConnection(nickname,url){
  const sio = io('', {
    transportOptions: {
      polling: {
        extraHeaders: {
          'X_USERNAME': nickname,
          'X_URL' : url
        }
      }
    }
  });

  //socket io
  sio.on('connect', () => {
  });

  sio.on('updateUserList', (userArr)=>{
    var UserListDiv = document.getElementById("nameSection");
    var name;  
    UserListDiv.innerHTML=""
    for (name of userArr){
      UserListDiv.innerHTML  += name+ "<br>"
      }
  });
  sio.on('disconnect', ()=>{
  });
  sio.on('user_joined', (userID)=>{
  });
  sio.on("Text_Message",(input)=>{
      var TheChatDiv = document.getElementById("chatBox"); //get the divider to later append to it
      TheChatDiv.innerText  +=  input  // SANITIZE INPUT
      TheChatDiv.innerHTML  +=  "<br>"
      var chatBox = document.getElementById("chatBox");
      chatBox.scrollTop= chatBox.scrollHeight; //after message sent, scroll down


    } );
  sio.on('user_left', (userID)=>{
  });
  sio.on('clientCounter', (counter)=>{
  });
  sio.on("updateUsers", (userlist)=>{
    document.getElementById('nameSection').innerHTML = null; //nullify list before updating it
    for (let key in userlist){ //loop the usernames dictionary
      
      document.getElementById('nameSection').innerHTML += key + "<br>"; //add name and break line after each user
    }
  });
  document.getElementById("button").addEventListener("click", getInput );
  //add enter press
  document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
      getInput();
    }
  });
  

  function getInput(){
    textFlag = document.getElementById("inpt").value;
    text = nickname+": " +document.getElementById("inpt").value; //get user text message
    if(textFlag){
        sio.emit("userInput", text); //send to server
        document.getElementById("inpt").value= null; //empty input box

    }
  }


}
 
 






