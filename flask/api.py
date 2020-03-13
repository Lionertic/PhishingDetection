from flask import Flask, request
from urlEncoder import process
from functions import editRow, addRow, trainModel, predict
import traceback

app = Flask(__name__)

@app.route("/check")
def check():
    try:
        url = request.args.get("url")

        if url == "":
            raise Exception("Wrong url")

        val = process(url)

        data = {}
        data["status"] = str(predict(val))

        return data, 200

    except Exception as e:
        l = traceback.format_exc()

        return {"status": -2}, 500


@app.route("/retrain")
def retrain():
    try:
        url = request.args.get("url")
        loc = int(request.args.get("loc"))
        feedback = int(request.args.get("feedback"))

        if feedback == 0:
            feedback = 1

        data = {}
        if loc == -1:
            app.logger.info(url)
            val = process(url)
            app.logger.info(val)

#             feedback =  feedback + int(predict(val))
            val[0].append(feedback)
            loc = addRow(val)
        else:
            editRow(feedback, loc)

        data['status'] = 1
        data['message'] = 'Retrained'
        data["location"] = loc

        return data, 200
    except Exception as e:
        l = traceback.format_exc()
        data = {}
        data['status'] = 0
        data['message'] = l
        return data, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
    trainModel()
