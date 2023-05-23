# For security reasons, parameters and data were changed or removed

import sqltesting
import socketio
import eventlet  #from eventlet import wsgi
sio = socketio.Server(cors_allowed_origins='*') #allow all cors. so chrome client can connect to diffferent domain such as my server

#Globals

IP = ''  
PORT = 0
counter =0 #users counter


global userCounter
global usersList
global sidToName
sidToName={}
userList = {}
userCounter = {}
app = socketio.WSGIApp(sio,static_files={ #html pages
                       '/':'./public/'
                       })


def AntiRandomRoom(sid,arr):
    
    for tavim in arr: #read strings
        if sid!=tavim: #if string is not sid
            return tavim #return url


@sio.event
def connect(sid, environ):
    global url
 

    username = environ.get('HTTP_X_USERNAME') 
    url = environ.get('HTTP_X_URL') 
    url = url.split('&')[0]
    sidToName[sid]=username

    sio.enter_room(sid,url)
    rooms = sio.rooms(sid)   
    
    #retrive messages
    HistoryLog=sqltesting.getHistory(url)
    for log in HistoryLog:
        sio.emit("Text_Message",log,to=(sid))

  
    #when client connect, tell its html to add him to the users list

    if url in userCounter:
        userList[url].append(username)
        userCounter[url]+=1
    else:
        userList[url]=[username]
        userCounter[url]=1
    #send userlist to js for update

    roomUrl = AntiRandomRoom(sid,sio.rooms(sid))
    sio.emit("updateUserList",userList[url],to=roomUrl)

@sio.event
def disconnect(sid):
    sqltesting.deleteOld()
    # global client_count

    exitingUser = sidToName.pop(sid)
    userList[url].remove(exitingUser)
    userCounter[url]-=1

    # if url has no users, delete the key    
    roomUrl = AntiRandomRoom(sid,sio.rooms(sid))
    sio.emit("updateUserList",userList[url],to=roomUrl)
    if userList[url]==[]: #if empty list 
        del userList[url]
        del userCounter[url]






@sio.event 
def userInput( sid , input): #user said something
    roomUrl = AntiRandomRoom(sid,sio.rooms(sid))
    sqltesting.addLog(input,roomUrl) #go log that message
    sio.emit("Text_Message",input,to=(roomUrl)) #send the full message to JS for printing

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((IP, PORT)), app) #start server

