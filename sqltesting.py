# For security reasons, parameters and data were changed to satire ones




import mysql.connector
from datetime import datetime



db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password", #fix this cringe behaviour later
    database="database"

)

myCursor = db.cursor()

#myCursor.execute("CREATE TABLE Logs2(Stamp VARCHAR(50),Day smallint UNSIGNED, Text VARCHAR(50), url VARCHAR(50))") 

def deleteOld():
    Day= datetime.now().day
    if Day==2:
        key_values = tuple(range(3, 31)) # Values from 3 to 31 (inclusive)
        delete_query = "DELETE FROM Logs2 WHERE Day IN (%s)" % (", ".join(["%s"] * len(key_values))) #last part = "%s"*27 days
        myCursor.execute(delete_query,key_values) 
    else:
        lastToDelete=Day-3
        key_values=tuple(range(lastToDelete)) #from 0 to last2delete
        print(f"deleting {key_values}")
        delete_query = "DELETE FROM Logs2 WHERE Day IN (%s)" % (", ".join(["%s"] * len(key_values))) 
        myCursor.execute(delete_query,key_values) 
    db.commit()



def addLog(text, url):
    print("writing to table")
    CurrentDate= datetime.now() 
    currentDay = CurrentDate.day
    # Format the timestamp as a string in the MySQL-compatible format
    timestamp_str = CurrentDate.strftime('%Y-%m-%d %H:%M:%S')
    myCursor.execute("INSERT INTO Logs2(Stamp, Day, Text, url) VALUES (%s,%s,%s,%s)" , (timestamp_str, currentDay, text, url))
    db.commit()


def getHistory(url):
    HistoryLog=["History Log"]
    HistoryLog.append("------------------")
    myCursor.execute("SELECT Text FROM Logs2 WHERE URL = %s ORDER BY Stamp", (url,)) # tuple
    text_logs = myCursor.fetchall()
    for log in text_logs:
        HistoryLog.append(log[0])
        
    HistoryLog.append("------------------")
    return HistoryLog


