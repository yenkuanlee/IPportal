from flask import Flask
from flask import request
from flask_cors import CORS
import ipfsapi
import json
import psycopg2
import requests
app = Flask(__name__)
CORS(app, resources=r'/*')
api = ipfsapi.connect('127.0.0.1','5001')

@app.route('/')
def index():
    return "Hello World!!"

@app.route('/Register', methods=['POST'])
def register():
    try:
        fhash = request.form['fhash']
        Rinfo = api.object_get(fhash)
        for x in Rinfo['Links']:
            if x['Name']=='Ehash':
                Ehash = api.object_get(x['Hash'])['Data']
            elif x['Name']=='Enode':
                Enode = api.object_get(x['Hash'])['Data']
            elif x['Name']=='ExternalIP':
                ExternalIP = api.object_get(x['Hash'])['Data']
            elif x['Name']=='peerID':
                peerID = api.object_get(x['Hash'])['Data']
        conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute("INSERT INTO BruceChain VALUES('"+Ehash+"','"+ExternalIP+"','"+Enode+"','"+peerID+"','"+Rinfo['Data']+"',0);")
        conn.commit()
        return json.dumps({"status": "Success"})
    except Exception as e:
        return json.dumps({"status": "Failed", "log": str(e)})

if __name__ == '__main__':
    app.run(host='172.16.0.156',port=8080, debug=True)
