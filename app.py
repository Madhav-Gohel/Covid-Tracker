import requests
from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    f_date = date(2020, 1, 27)
    l_date = date.today()
    delta = l_date - f_date
    days = delta.days
    print(days)
    historical_data = requests.get("https://disease.sh/v3/covid-19/historical/IN?lastdays="+str(days)).json()
    dates = str(historical_data["timeline"]["cases"].keys()).replace("dict_keys([","").replace("])","").replace("'","").split(', ')
    cases = str(historical_data["timeline"]["cases"].values()).replace("dict_values([","").replace("])","").split(', ')
    deaths = str(historical_data["timeline"]["deaths"].values()).replace("dict_values([","").replace("])","").split(', ')
    recovered = str(historical_data["timeline"]["recovered"].values()).replace("dict_values([","").replace("])","").split(', ')
    countries_data = requests.get("https://disease.sh/v3/covid-19/countries").json()
    state_data = requests.get("https://disease.sh/v3/covid-19/gov/IND").json()
    covid_news = requests.get("https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=72bc559de1ab411ca00958d70ec3f1d5").json()
    daily_cases = []
    daily_deaths = []
    daily_recovered = []
    daily_cases.append(cases[0])
    for x in range(len(cases)+1):
        if x+1 == len(cases):
            break
        daily_cases.append(int(cases[x+1])-int(cases[x]))
    daily_deaths.append(deaths[0])
    for i in range(len(deaths)+1):
        if i+1 ==len(deaths):
            break
        daily_deaths.append(int(deaths[i+1])-int(deaths[i]))
    daily_recovered.append(recovered[0])
    for i in range(len(recovered)+1):
        if i+1 ==len(recovered):
            break
        daily_recovered.append(int(recovered[i+1])-int(recovered[i]))
    return render_template("index.html",dates=dates,cases=cases,n=days,deaths=deaths,recovered=recovered,countries_data=countries_data,state_data=state_data,daily_cases=daily_cases,daily_deaths=daily_deaths,daily_recovered=daily_recovered,news=covid_news)

