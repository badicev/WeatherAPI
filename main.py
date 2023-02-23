import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
stations = pd.read_csv("data/data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("index.html", data=stations.to_html())


@app.route("/api/v1/annual/<station>/<year>")
def yearly(station, year):
    filename = "data/data_small/TG_STAID" + str(station).zfill(
        6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict()
    return result


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    df = pd.read_csv(
        r"data\data_small\TG_STAID" + str(station).zfill(
            6) + ".txt", skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data/data_small/TG_STAID" + str(station).zfill(
        6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = str(df.to_dict(orient="records"))
    return result


if __name__ == "__main__":  # only run when this script is executed
    app.run(debug=True)
