import json
import cv2
import numpy as np
import flask
from flask import Flask,url_for,render_template,request,redirect,send_file,jsonify

app = Flask(__name__)
app.config["global_OK"] = "ok"
app.config["cnt"] = 0
app.config["show_image"] = True

# only post result of json
@app.route('/api_show_info' , methods=['POST'])
def api_show_info():
    info = request.json
    print(json.dumps(info,indent=4))
    return jsonify(app.config["global_OK"])

# post image and json on the same
@app.route('/api_show_image' , methods=['POST'])
def api_show_image():
    # get the detect result with json format
    info = request.form.to_dict()['result']
    info = json.loads(info)
    # print(json.dumps(info,indent=4))

    if app.config["show_image"]:
        npimg = np.fromfile(request.files['image'], np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        cv2.imshow("frames",frame)
        cv2.waitKey(1)
    
    return jsonify(app.config["global_OK"])

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=7008,threaded=False)
