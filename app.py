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

    historical_data = requests.get(
        "https://disease.sh/v3/covid-19/historical/IN?lastdays=" + str(days)
    ).json()

    # Safeguard missing categories
    timeline = historical_data.get("timeline", {})
    cases_dict = timeline.get("cases", {})
    deaths_dict = timeline.get("deaths", {})
    recovered_dict = timeline.get("recovered", {})

    dates = list(cases_dict.keys())
    cases = list(cases_dict.values())
    deaths = list(deaths_dict.values())
    recovered = list(recovered_dict.values())

    countries_data = requests.get("https://disease.sh/v3/covid-19/countries").json()
    state_data = requests.get("https://disease.sh/v3/covid-19/gov/IND").json()
    covid_news = requests.get(
        "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=72bc559de1ab411ca00958d70ec3f1d5"
    ).json()

    daily_cases = []
    daily_deaths = []
    daily_recovered = []

    def build_daily_metric(base_list):
        if not base_list:
            return []
        daily = [base_list[0]]
        for i in range(1, len(base_list)):
            daily.append(int(base_list[i]) - int(base_list[i - 1]))
        return daily

    daily_cases = build_daily_metric(cases)
    daily_deaths = build_daily_metric(deaths)
    daily_recovered = build_daily_metric(recovered)

    return render_template(
        "index.html",
        dates=dates,
        cases=cases,
        n=days,
        deaths=deaths,
        recovered=recovered,
        countries_data=countries_data,
        state_data=state_data,
        daily_cases=daily_cases,
        daily_deaths=daily_deaths,
        daily_recovered=daily_recovered,
        news=covid_news,
    )
