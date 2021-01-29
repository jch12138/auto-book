#!flask/bin/python
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app,supports_credentials=True)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/set_seat')
def book():

    value = request.args.get("value")
    # method = request.args.get("method")
    
    # print(user_id, method)
    # print(value,type(value))
    try:
        # res = process(user_id,method)
        if value == '1':
            with open ('seat_info.txt','w')as f:
                f.write('4522 010\n4522 005')
            res = True
        elif value == '2':
            with open ('seat_info.txt','w')as f:
                f.write('4519 018\n4519 008')
            res = True
        else:
            res = False
    except:
        res = False

    response = {
        'status':res
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=4321)