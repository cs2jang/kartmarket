from flask import Flask, request, jsonify
from gdata import GS
import json

app = Flask(__name__)
 
@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()
    print(user)
    print('==============================')
    print(jsonify(user))
    return jsonify(user)
 
@app.route('/getMenu', methods = ['POST'])
def getMenu():
    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']
    user_req_date = json.loads(user_detail['sys_date']['value'])

    gs_conn = GS()
    res_menu = gs_conn.getGSMenu(user_req_date['date'])

    res_dict = dict()
    res_dict["version"] = "2.0"
    res_dict["template"] = {
        "outputs" : [
            {
                "simpleText" : {
                    "text" : res_menu
                }
            }
        ]
    }
    print(res_dict)
    return jsonify(res_dict)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55005)
