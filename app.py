from flask import Flask, request, jsonify
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
    user_said = req_dict['userRequest']['utterance']
    user_detail = req_dict['action']['detailParams']
    user_req_date = user_detail['sys_date']
    user_req_menu = user_detail['kart_menu']

    print(user_said, user_req_date, user_req_menu)
    res_dict = dict()
    res_dict['version'] = "1.0"
    res_dict['template'] = {
        'output' : [
            {
                'simpleText' : {
                    'text' : "오늘의 메뉴는 맛있는 밥입니다아!"
                }
            }
        ]
    }
    print('return is ' + jsonify(res_dict))
    return jsonify({res_dict})

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55005)