from flask import Flask, render_template, json, request, jsonify, send_from_directory
#from flask.ext.mysql import MySQL
from collections import namedtuple
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'Matchup'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route("/")
def main():
    return render_template('login.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("insert into users (name, email, password) values (_name, _email,_password )")
    data = cursor.fetchone()
    cursor.close

@app.route("/signUp",methods=['GET'])
def newUser():
    return render_template('signup.html')

@app.route('/getMatchedProfiles',methods=['GET'])
def getMatchedProfiles():
    #data = request.get_json()
    #print("Event Data:",data)
    #profile_id = data['Profile_Id']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT B.Profile_ID as 'Match', COUNT(*) as 'Strength' FROM (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` WHERE Profile_ID = '4' )A JOIN (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` WHERE Profile_ID <> '4') B ON A.Topic_ID = B.Topic_ID GROUP BY B.Profile_ID ORDER BY COUNT(*) DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    pplList= []
    for i in range(0,len(results)):
        pplList.append(results[i][0])
    print(pplList)
    var_string = ','.join(['%s'] * len(pplList))
    cursor.execute("Select * from Matchup.Profile where Profile_ID IN (%s)" % var_string,
                tuple(pplList))
    matchedPplResults = cursor.fetchall()

    newresultlist = []
    for i in range(0, len(results)):
        for j in range(0, len(matchedPplResults)):
            if(results[i][0] == matchedPplResults[j][0]):
                newresult = []
                newresult.append(matchedPplResults[j][0])
                newresult.append(matchedPplResults[j][1])
                newresult.append(matchedPplResults[j][2])
                newresult.append(matchedPplResults[j][3])
                newresult.append(matchedPplResults[j][4])
                newresult.append(matchedPplResults[j][5])
                newresult.append(matchedPplResults[j][6])
                newresult.append(matchedPplResults[j][7])
                newresult.append(matchedPplResults[j][8])
                newresult.append(matchedPplResults[j][9])
                newresult.append(matchedPplResults[j][10])
                newresult.append(matchedPplResults[j][11])
                newresult.append(results[i][1])
                newresultlist.append(newresult)
                #newlist = matchedPplResults[j] + newresult[1]
                
        #print(results[i][0])
        #print(matchedPplResults[i][0])
    print("fas:",newresult)
    cursor.execute("SELECT A.Person, B.Topic AS 'Topic' FROM (   SELECT B.Profile_ID as 'Person', B.Topic_ID as 'Topic' FROM (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests`  WHERE Profile_ID = '4' )A JOIN (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests`  WHERE Profile_ID <> '4') B ON A.Topic_ID = B.Topic_ID ORDER BY B.Profile_ID DESC) A  JOIN  `Matchup`.`Topics` B  ON A.Topic = B.Topic_ID ORDER BY A.Person")
    matchedInterests = cursor.fetchall()
    #newlist = tuple(matchedPplResults) + tuple (matchedInterests)
    #print(newlist)

    #print(matchedInterests)
    d = {}
    for i in range(0,len(matchedInterests)):
        if matchedInterests[i][0] in d:
            l = []
            l.append(d.get(matchedInterests[i][0]))
            l.append(matchedInterests[i][1])
            d[matchedInterests[i][0]] = l
        else:
            d[matchedInterests[i][0]] = matchedInterests[i][1]
    print(d)

    finalResultList = []
    for i in range(0, len(newresultlist)):
        for key in d:
            if newresultlist[i][0] == key:
                newresult = []
                newresult.append(newresultlist[i][0])
                newresult.append(newresultlist[i][1])
                newresult.append(newresultlist[i][2])
                newresult.append(newresultlist[i][3])
                newresult.append(newresultlist[i][4])
                newresult.append(newresultlist[i][5])
                newresult.append(newresultlist[i][6])
                newresult.append(newresultlist[i][7])
                newresult.append(newresultlist[i][8])
                newresult.append(newresultlist[i][9])
                newresult.append(newresultlist[i][10])
                newresult.append(newresultlist[i][11])
                newresult.append(newresultlist[i][12])
                newresult.append(d.get(key))
                finalResultList.append(newresult)

    cursor.close
    #return jsonify(finalResultList)
    return render_template('Matches.html', data=finalResultList)

@app.route('/userProfile',methods=['GET'])
def getUserProfile():
    return render_template('profile.html')

@app.route('/getuser',methods=['GET'])
def getUser():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM Profile"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Matches.html', data=results)

@app.route('/events',methods=['GET'])
def getEvent():
    
    event = namedtuple("event", "name location time strength interests")
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM Event"
    cursor.execute(sql)
    results = cursor.fetchall()
    sql = """SELECT D.Name, C.Strength FROM (
SELECT B.Event_ID as 'Event', COUNT(*) as 'Strength' FROM (
SELECT Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Event_ID, Topic_ID from `Matchup`.`Event_Topics` 
) B
ON A.Topic_ID = B.Topic_ID
GROUP BY B.Event_ID
ORDER BY COUNT(*) DESC) C
JOIN
(SELECT * FROM `Matchup`.`Event`) D
ON C.Event = D.Event_ID;"""
    cursor.execute(sql)
    results2 = cursor.fetchall()
    sql = """SELECT X.Name, Y.Topic FROM (
SELECT C.Name, D.Topic_ID FROM (
SELECT B.Event_ID  as 'Event' , B.Topic_ID FROM (
SELECT Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Event_ID, Topic_ID from `Matchup`.`Event_Topics` ) B
ON A.Topic_ID = B.Topic_ID
) D 
JOIN 
(SELECT * FROM `Matchup`.`Event` ) C
ON D.Event = C.Event_ID) X
JOIN 
(SELECT * FROM `Matchup`.`Topics` ) Y
ON X.Topic_ID = Y.Topic_ID
ORDER BY X.NAME;"""
    cursor.execute(sql)
    results3 = cursor.fetchall()
    L = []
    notin = ""
    for item in results2:
        for i2 in results:
            topics = ""
            if (i2[1] == item[0]):
                notin += i2[0] + ", "
                for i3 in results3:
                    if (i3[0] == item[0]):
                        topics += i3[1] + ", "
                topics = topics[0: len(topics)-2]
                e = event(item[0],i2[2], i2[3], item[1], topics)
                L.append(e)
    notin = notin[0: len(notin)-2]
    sql = "SELECT * FROM `Matchup`.`Event` WHERE Event_ID not in (" + notin  + ")"
    cursor.execute(sql)
    resultsnotin = cursor.fetchall()
    for item in resultsnotin:
        e = event(item[1],item[2], item[3], None, None)
        L.append(e)
    
    return render_template('index.html', data=L)


if __name__ == "__main__":
    app.run()



