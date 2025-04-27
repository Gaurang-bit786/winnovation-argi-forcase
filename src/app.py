import json
import pickle
import pandas as pd 
from random import random
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
fp.close()

df = pd.read_csv("../final_merged_dataset (1).csv")

@app.route('/', methods=['GET'])
def dashboard():
    print(df[:2].to_json(orient='records'))
    return render_template('dashboard.html',common_data={
        "dist_length":len(common_data['district'].keys()),
        "var_length":len(common_data['variety'].keys()),
        "market_length":len(common_data['market'].keys()),
        "comm_length":len(common_data['commodity'].keys()),
        "grade_length":len(common_data['grade'].keys()),
        "data":df[:30].to_dict(orient='records')
    })



@app.route('/prediction', methods=['GET', 'POST'])
def pridect():
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
        return render_template('prediction.html',common_data=common_data)
    return render_template('prediction.html',common_data=common_data)


@app.route('/create-record', methods=['GET', 'POST'])
def creat_data():
    if request.method == 'POST':
        print(request.form)
        df = pd.DataFrame({
            "District Name":request.form.get("district"),
            "Market Name":request.form.get("market"),
            "Commodity":request.form.get("commodity"),
            "Variety":request.form.get("variety"),
            "Grade":request.form.get("grade"),
            "Min Price (Rs./Quintal)":request.form.get("min_price"),
            "Max Price (Rs./Quintal)":request.form.get("max_price"),
            "Modal Price (Rs./Quintal)":request.form.get("modal_price"),
            "Price Date":request.form.get("date"),
            "Temperature":request.form.get("tempt")
        })
        print(df)
        df.to_csv('../final_merged_dataset (1).csv',mode='a', header=False, index=False)
        return render_template('create-data.html',common_data=common_data)
    return render_template('create-data.html',common_data=common_data)



if __name__=="__main__":
    app.run(debug=True)