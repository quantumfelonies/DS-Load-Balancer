import os
from flask import Flask, jsonify,request,Response
from requests import get
import requests


class Mapper:
    hashmap=[]

CMapp=Mapper()

app = Flask(__name__)


@app.route('/rep', methods=['GET'])
def rep():
    return jsonify({"message" : {"N" : len(CMapp.hashmap),"replicas" : CMapp.hashmap} ,"status" : "successful"})

@app.route('/add', methods=['POST'])
def add():
    json_data = request.get_json()
    print(json_data)
    if( not json_data['n']==len(json_data['hostnames'])):#Check if the number of required hostnames matches the number of hostnames
        print('Extra unnamed containers will be created')
    else:
        for hostname in json_data['hostnames']:
            print('running:','docker run -p 80:5001 --name containerB -e VAR1=v1 -e VAR2=v2 -d a0-server:latest')
    
    return jsonify({'message':{"N" : len(CMapp.hashmap),"replicas" : CMapp.hashmap},"status" : "successful"})



@app.route('/add_test', methods=['POST'])
def add_test():
    json_data     = request.get_json()
    print(json_data)
    res=os.popen('docker run -p 5001:5001 --name test_container -e port=5001 -e ID=1 -d master_flask_copy:latest').read()
    if len(res)==0:
        print("Unable to start test_container")
    else:
        print("successfully started test_container")
    return jsonify({'message':{"N" : len(CMapp.hashmap),"replicas" : CMapp.hashmap},"status" : "successful"})



@app.route('/rm', methods=['POST'])
def rm():
    json_data     = request.get_json()
    print(json_data)
    try:
        os.system('docker stop test_container && docker rm test_container')
    except:
        print('Error trying to close container')
    return jsonify({"message" : {"N" : 4,"replicas" : ["Server 1", "Server 3", "S10", "S11"]},"status" : "successful"})


@app.route('/<path>')
def proxy1(path):
    print(request.cookies.get('server_id'))
    if(request.cookies.get('server_id')==None):
        print('Rerouting to the next slot alocatable')
    else:
        print('Rerouting to the same ')


    #Call the hash map here


    res = requests.request(
        method          = request.method,
        url             = request.url.replace(request.host_url, 'http://host.docker.internal:5001/'),
        headers         = {k:v for k,v in request.headers if k.lower() != 'host'},
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']  
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    response = Response(res.content, res.status_code, headers)
    response.set_cookie('server_id','0')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
