
import logging
from flask import Flask, jsonify
from flask import request
from multiprocessing import Process
import json, os, signal
import pymongo
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]


@app.route('/')
def index():
    return "First"


@app.route('/record', methods=['GET'])
def record():
    mydict = { "name": request.args.get('name'), "surname": request.args.get('surname') }
    x = mycol.insert_one(mydict)

    return "Data Recorded"


@app.route('/start',methods = ['POST'])
def another():
    return request.data

@app.route("/shutdown", methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })


if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0')

