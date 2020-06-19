import os
from os import walk
import sys
import argparse
import imghdr
from flask import Flask, render_template, url_for, send_file, redirect, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Configure Db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/webpage',methods=['GET','POST'])
def webpage():
    if(app.config["HEAD"] == len(app.config["FILES"])):
        exit()
    not_end = not(app.config["HEAD"] == len(app.config["FILES"]) - 1)
    image = app.config["FILES"][app.config["HEAD"]]
    directory = app.config["IMAGES"]
    if request.method == 'POST':
        label = request.form['label']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO image_labels(image,label) VALUES(%s, %s)", (image, label))
        mysql.connection.commit()
        cur.close()
    return render_template("webpage.html", not_end=not_end, directory=directory, image=image, head=app.config["HEAD"]+1, len=len(app.config["FILES"]) )

@app.route('/next')
def next():
    image = app.config["FILES"][app.config["HEAD"]]
    app.config["HEAD"] = app.config["HEAD"] + 1
    return redirect(url_for('webpage'))

@app.route('/image/<f>')
def images(f):
    images = app.config['IMAGES']
    return send_file(images + f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='specify input image directory')
    args = parser.parse_args()
    directory = args.dir
    if directory[len(directory) - 1] != "/":
        directory += "/"
    app.config["IMAGES"] = directory
    files = None
    for(dirpath, dirnames, filenames) in walk(app.config["IMAGES"]):
        files = filenames
        break
    if files == None:
        print("No Files")
        exit()
    app.config["FILES"] = files
    app.config["HEAD"] = 0
    app.run(debug=True)
