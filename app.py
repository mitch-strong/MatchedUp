from flask import Flask, render_template, json, request, jsonify
#from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'Matchup'
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
    print(data2)
    return 'Success'


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



