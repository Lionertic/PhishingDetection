from flask import Flask, request
from urlEncoder import process
from functions import editRow, addRow, trainModel, predict
import traceback
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

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

        data = {}
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


@scheduler.task('interval', id='training', minutes=5 )
def training():
    app.logger.info('Training starts')
    trainModel()

# # @scheduler.task('interval', id='do_job_1', seconds=30)
# def chcel():
#     print(scheduler.get_job("training"))
#     app.logger.info(scheduler.get_job("training"))

if __name__ == "__main__" :
    trainModel()
    scheduler.start()
    app.run(host='0.0.0.0', debug=False, port=80)
