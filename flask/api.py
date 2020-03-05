from flask import Flask, request
from urlEncoder import process
import joblib
from functions import editRow, addRow

app = Flask(__name__)

@app.route("/check")
def check():
    try:
        url = request.args.get("url")
        
        if url == "":
            raise "Wrong url"

        val = process(url)

        model = joblib.load("model.pkl")
        pred = model.predict(val)

        if pred >= 0 :
            data = {'message': 'Its good url'}
        else:
            data = {'message': 'Its phishing url'}

        return data ,200

    except Exception as e:
        return e, 500

@app.route("/retrain")
def retrain():
    try:
        url = request.args.get("url")
        loc = int(request.args.get("loc"))
        feedback = int(request.args.get("feedback"))

        if feedback == 0 :
            feedback = 1
        
        data = {}
        if loc == -1:
            val = process(url)
            val[0].append(feedback)
            pos = addRow(val)
            data["location"] = pos
        else:
            editRow(feedback,loc)
            data["location"] = loc
        
        return data, 200
    except Exception as e:
        return {"message" : "err"  }, 500 
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)