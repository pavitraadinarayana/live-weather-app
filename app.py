from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "16d992dd54636ad325883c23b426a241"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = {
                "city":        data["name"],
                "country":     data["sys"]["country"],
                "temp":        round(data["main"]["temp"], 1),
                "feels_like":  round(data["main"]["feels_like"], 1),
                "humidity":    data["main"]["humidity"],
                "wind":        data["wind"]["speed"],
                "description": data["weather"][0]["description"].title(),
                "icon":        data["weather"][0]["icon"],
            }
        else:
            error = "City not found! Please try again."

    return render_template("index.html",
                           weather=weather,
                           error=error)

if __name__ == "__main__":
    app.run(debug=True)