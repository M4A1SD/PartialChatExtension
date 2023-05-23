
var nickname;
const animals = [
  "Dog",
  "Cat",
  "Elephant",
  "Lion",
  "Tiger",
  "Giraffe",
  "Monkey",
  "Kangaroo",
  "Horse",
  "Cow",
  "Pig",
  "Sheep",
  "Goat",
  "Rabbit",
  "Mouse",
  "Bear",
  "Deer",
  "Fox",
  "Wolf",
  "Zebra",
  "Dolphin",
  "Whale",
  "Octopus",
  "Penguin",
  "Squirrel",
  "Owl",
  "Eagle",
  "Crocodile",
  "Turtle",
  "Gorilla"
];

async function setName() {
  return new Promise((resolve, reject) => {
    chrome.storage.session.get(["nickname"], async (result) => {
      if (Object.keys(result).length === 0) {
        let random = Math.floor(Math.random() * 30);
        nickname = animals[random];
        await chrome.storage.session.set({ "nickname": nickname });
        resolve(nickname);
      } else {
        nickname = result["nickname"];
        resolve(nickname);
      }
    });
  });
}




chrome.runtime.onMessage.addListener(async function(message, sender, sendResponse) {
  if (message.action === 'getUrl') {
    const [currentTab] = await chrome.tabs.query({ active:true ,  lastFocusedWindow: true });
    var url = currentTab.url; //video URL doenst work in debugger. async
    //hard to debug because its async so i doesnt load fast in the debugger
    const prefix = "https://www.youtube.com/watch?v=";
    if (url.startsWith(prefix)) {
      url = url.slice(32); //ignore http:youtube/video=
    }
    else{
      url = "xxxxxxxxxxx"
    }
    nickname= await setName();
    chrome.runtime.sendMessage({ vidID: url, IGN : nickname });

  }
});

