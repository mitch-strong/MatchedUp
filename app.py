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
    return "Welcome!"

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



