import traceback
from flask_apscheduler import APScheduler
from functions import editRow, addRow, trainModel, predict
from urlEncoder import process

from flask import Flask, request

app = Flask(__name__)
scheduler = APScheduler()


@app.route("/check")
def check():
    try:
        url = request.args.get("url")
        if url == "":
            raise Exception("Wrong url")

        val = process(url)

        return {"status": str(predict(val))}, 200

    except Exception as e:
        return {"status": -2}, 500


@app.route("/retrain")
def retrain():
    try:
        url = request.args.get("url")
        loc = int(request.args.get("loc"))
        feedback = int(request.args.get("feedback"))

        if loc == -1:
            val = process(url)
            val[0].append(feedback)
            loc = addRow(val)
        else:
            editRow(feedback, loc)

        return {'status': 1, 'message': 'Retrained', "location": loc}, 200

    except Exception as e:
        data = {'status': 0, 'message': traceback.format_exc()}
        return data, 500


@scheduler.task('interval', id='training', minutes=5 )
def training():
    app.logger.info('Training starts')
    trainModel()


if __name__ == "__main__" :
    trainModel()
    scheduler.start()
    app.run(host='0.0.0.0', debug=False, port=80)
