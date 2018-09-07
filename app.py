from flask import Flask, render_template, json, request, jsonify
#from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'matchup'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

# App Functions
@app.route("/")
def main():
    return "Welcome!"

@app.route('/signUp',methods=['POST'])
def signUp():
    
    data = request.get_json()
    print(data)
    # read the posted values from the UI

    print("test2",data['Name'])
    _name = data['Name']
    gender = data['Gender']
    dob = data['DOB']
    _password = data['Password']
    fromCity = data['From_City']
    newCity = data['New_City']
    school = data['School']
    language = data['Language']
    major = data['Major']
    email = data['Email']

    print("All:",_name, email, _password)

    conn = mysql.connect()
    cursor =conn.cursor()
    sql = "INSERT INTO `Matchup`.`Profile` (Name,Email,Password,Gender,DOB,From_City,New_City,School,Language,Major,Local) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #sql = "insert into users (name, email, password) values (%s,%s,%s)"
    cursor.execute(sql, (_name,email,_password,gender, dob, fromCity, newCity, school,language,major,1 ))
    conn.commit()
    data2 = cursor.lastrowid
    varlist = [1,2]
    for i in range(0,len(varlist)):

    #var_string = ', '.join('?' * len(varlist))
        query_string = 'INSERT INTO `Matchup`.`Interests`(Profile_ID,Topic_ID) VALUES (%s,%s)'
        cursor.execute(query_string, (data2, varlist[i]))
        conn.commit()
    return 'Success'

@app.route('/createEvent',methods=['POST'])
def createEvent():
    data = request.get_json()
    print("Event Data:",data)
    # read the posted values from the UI
    conn = mysql.connect()
    cursor =conn.cursor()

    sql = "INSERT INTO `Matchup`.`Event` (Name,Location,Time) values (%s,%s,%s)"

    cursor.execute(sql, (data['Name'],data['Location'],data['Time'] ))
    conn.commit()
    data2 = cursor.lastrowid
    print(data2)
    return 'Success'

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
    return jsonify(finalResultList)

@app.route('/getuser',methods=['GET'])
def getUser():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)


if __name__ == "__main__":
    app.run()



