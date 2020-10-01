from datetime import datetime as dt
from flask import Flask, request, jsonify, render_template
from gdata import GS
import json

app = Flask(__name__)

@app.route('/getThisWeekPage')
def getThisWeekPage():
    return render_template('thisweek.html')

 
@app.route('/getWeekly', methods = ['POST'])
def getWeekly():
    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']
    print('==============================')
    print(user_detail)
    # user_req_date = json.loads(user_detail['sys_date']['value'])
    
    return jsonify(user_detail)
 
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
    return jsonify(res_dict)

@app.route('/setExcept', methods = ['POST'])
def setExcept():
    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']    
    user_req_num = json.loads(user_detail['몇명']['value'])
    user_req_num = int(user_req_num['amount'])
    gs_conn = GS()
    result_text = gs_conn.setExceptPeople(user_req_num)

    res_dict = dict()
    res_dict["version"] = "2.0"
    res_dict["template"] = {
        "outputs" : [
            {
                "simpleText" : {
                    "text" : result_text
                }
            }
        ]
    }
    return jsonify(res_dict)

@app.route('/getExcept', methods = ['POST'])
def getExcept():    
    gs_conn = GS()
    result_text = gs_conn.getExceptPeople()

    res_dict = dict()
    res_dict["version"] = "2.0"
    res_dict["template"] = {
        "outputs" : [
            {
                "simpleText" : {
                    "text" : result_text
                }
            }
        ]
    }
    return jsonify(res_dict)
    
@app.route('/')
def hello_world():
    return 'Hello, World!'
    
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55005)
