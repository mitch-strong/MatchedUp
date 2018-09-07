from flask import Flask, render_template, json, request, jsonify, send_from_directory
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

    #return jsonify(results)


if __name__ == "__main__":
    app.run()



