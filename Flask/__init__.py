import mysql.connector

from flask import Flask, request, jsonify, redirect, render_template, url_for

def log(func):
    def wrapper(*args, **kwargs):
        func_str = func.__name__
        args_str = '\t '.join(args)
        with open('LOG_scrapp.log', 'w') as f:
            f.write(func_str)
            f.write(args_str)
        return func(*args, **kwargs)
    return wrapper



app = Flask(__name__)


def createConnection():
    c = mysql.connector.connect(
            host='scrapping_database_1',
            user='root',
            password='pwd',
            auth_plugin='mysql_native_password',
            database='vintage_ride'
    )
    return c


@log
@app.route("/")
def home():
    return "home"


@log
@app.route('/api', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
       dest = request.form['destination']
       d1 = request.form['date_begin']
       d2 = request.form['date_end']
       y = request.form['year']
       if not dest:
           return redirect(url_for('searching_dates', d1=d1, d2=d2))

        elif not d1 and not d2:
            return redirect(url_for('searching-dest', dest=dest))

    else:
        return render_template('api.html')

        
@log
@app.route('/searching-dest/<dest>', methods=['POST', 'GET'])
def search_dest(dest):
    c = createConnection()
    cur = c.cursor()
    cur.execute('use vintage_ride')
    cur.execute("SELECT * FROM vintage_ride WHERE destination LIKE %s;", (dest))
    results = cur.fetchall()
    return render_template("results.html", results=results)
    if request.method == 'POST':
        mail = request.form["mail"]
        if not mail:
            return redirect(url_for('searching-dest', dest=dest))
        else:
            mailing()
            return render_template('api.html')




@log
@app.route('/searching-dates/<d1>/<d2>/<y>', methods=['POST', 'GET'])
def search_dates(d1, d2, y):
    c = createConnection()
    cur = c.cursor()
    cur.execute('use vintage_ride')
    cur.execute("SELECT * FROM vintage_ride WHERE departure_date<=%s AND end_date>=%s AND year LIKE %s;", (d1, d2, y))
    results = cur.fetchall()
    return render_template("results.html", results=results)
    if request.method == 'POST':
        mail = request.form["mail"]
        if not mail:
            return redirect(url_for('searching-dates', d1=d1, d2=d2, y=y))
        else:
            mailing()
            return render_template('api.html')





# def get_data():
#     c = mysql.connection.cursor()
#     c.execute('use vintage_ride')
#     c.execute('''select * from vintage_ride''')
#     data = c.fetchall()
#     return render_template("qzoriejuf.html", data=data")
#     # vintage_ride = []
#     # content = {}
#     # for result in data:
#     #     content = {'ID': result['ID'], 'title': result['title'], 'destination': result['destination'], 'departure_date': result['departure_date'], 'end_date': result['end_date'], 'year': result['year'], 'level': result['level']}
#     #     vintage_ride.append(content)
#     #     content = {}
#     mysql.connection.commit()
#     c.close()
    
#     return jsonify(data)





#Emailing:

import smtplib, ssl
import threading

def mailing():
    sender_mail = "test@gmail.com"
    dest_mail = "merelle@gmail.com"
    password = input(str("Enter your mail password: "))
    message = "we have a match !! "

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("logging sender_mail success")
    server.sendmail(sender_mail, dest_mail, message)
    print("mail has been send to ", dest_mail)
    server.quit()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=4000, debug = True)