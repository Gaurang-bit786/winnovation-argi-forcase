import json
import pickle
import pandas as pd 
from flask import Flask, request, render_template


fp1 = open("../data/district_data.json")
fp2 = open("../data/commodity_data.json")
fp3 = open("../data/vaierty_data.json")
fp4 = open("../data/grade_data.json")
fp5 = open("../data/market_data.json")


district_data = json.load(fp1)
commodity_data = json.load(fp2)
vaierty_data = json.load(fp3)
grade_data = json.load(fp4)
market_data = json.load(fp5)

app = Flask(__name__)

common_data = {
            "district":dict(district_data),
            "commodity":dict(commodity_data),
            "variety":dict(vaierty_data),
            "grade":dict(grade_data),
            "market":dict(market_data)
        }

fp = open('../model/random_forest_model.pkl', 'rb')
model = pickle.load(fp)
print(model.predict([[11,2022,0,7,0,38,2]]))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prediction_data = []
        values = list(dict(request.form).values())
        prediction_data.append(
            request.form.get('month').split("-")[1]
        )
        prediction_data.append(
            request.form.get('month').split("-")[0]
        )
        prediction_data.extend(values[1:])
        common_data['predict'] = model.predict([prediction_data])[0]
        return render_template('index.html',common_data=common_data)
    return render_template('index.html',common_data=common_data)


if __name__=="__main__":
    app.run(debug=True)