from flask import Flask, request, jsonify
app = Flask(__name__)
 
@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()
    return jsonify(user)
 
@app.route('/environments/<language>')
def environments(language):
    return jsonify({"language":language})

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
 
if __name__ == "__main__":
    app.run(port=55005)
