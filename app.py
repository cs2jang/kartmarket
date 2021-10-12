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

    return render_template('thisweek.html', date_list=zip(result_dict['date_nums'], result_dict['date_string']), menu_list=result_dict['menus'])

 
@app.route('/getWeekly', methods = ['POST'])
def getWeekly():
    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']

    res_dict = dict()
    res_dict["version"] = "2.0"
    res_dict["template"] = {
        "outputs" : [
            {
                "basicCard" : {
                    "title": "이번 주 식단",
                     "buttons": [
                        {
                        "action": "webLink",
                        "label": "이번 주 식단 확인",
                        "webLinkUrl": "https://kartmarket.herokuapp.com/getThisWeekPage"
                        },
                     ]
                }
            }
        ]
    }
    
    return jsonify(res_dict)
 
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
    res_dict = dict()
    res_dict["version"] = "2.0"
    target_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if int(target_date[11:13]) > 9:
        res_dict["template"] = {
            "outputs" : [{
                "basicCard" : {
                    "title" : '제외 가능 신청 시간이 지났습니다.(오전 9시까지)', 
                    "buttons": [{
                        "action": "phone",
                        "label": "조리사님 연락하기",
                        "phoneNumber": "01032510770"
                        }]
                    }
            }]
        }
        return jsonify(res_dict)

    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']    
    user_req_num = json.loads(user_detail['몇명']['value'])
    user_req_num = int(user_req_num['amount'])
    gs_conn = GS()
    result_text = gs_conn.setExceptPeople(user_req_num)

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


@app.route('/getSample', methods = ['POST'])
def getSample():    
    gs_conn = GS()
    result_text = gs_conn.getSample()

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
    
@app.route('/getSampleLink', methods = ['POST'])
def getSampleLink():
    req_dict = request.get_json()
    user_detail = req_dict['action']['detailParams']

    res_dict = dict()
    res_dict["version"] = "2.0"
    res_dict["template"] = {
        "outputs" : [
            {
                "basicCard" : {
                    "title": "샘플마트로 연결",
                     "buttons": [
                        {
                        "action": "webLink",
                        "label": "샘플마트로 연결",
                        "webLinkUrl": "https://kko-ch-ecommerce.herokuapp.com"
                        },
                     ]
                }
            }
        ]
    }
    
    return jsonify(res_dict)
    
 
if __name__ == "__main__":
    app.run(port=55005, debug=False)
    # app.run(host='0.0.0.0', port=55005, debug=False)
