from datetime import datetime, timedelta, date
from flask import Flask, request, jsonify, render_template
from gdata import GS
import json

app = Flask(__name__)

@app.route('/getThisWeekPage')
def getThisWeekPage():
    monday = date.today() + timedelta(days=-date.today().weekday(), weeks=0)

    result_dict ={'date_nums': [], 'date_string': [], 'menus': []}
    
    gs_conn = GS()
    for i in range(5):
        if i == 0:
            date_num = monday
        else:
            date_num = monday + timedelta(days=i)

        date_string = date_num.strftime("%A")
        menu = gs_conn.getGSMenu(date_num.strftime("%Y-%m-%d"))

        result_dict['date_nums'].append(date_num.strftime("%Y-%m-%d"))
        result_dict['date_string'].append(date_string)
        result_dict['menus'].append(menu)

        # text_form = f'{date_num} {date_string} \n {menu}'
        # result_list.append(text_form)

    return render_template('thisweek.html', menu_dict=result_dict)

 
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
