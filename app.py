from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def normalize(text):
    return str(text).replace(" ", "").lower()

@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        keyword = request.form.get("name", "").strip()

        df = pd.read_excel("price.xlsx")

        df["_key"] = df["name"].apply(normalize)
        key = normalize(keyword)

        results = df[df["_key"].str.contains(key)]

        # 🔽 여기 반드시 if 안에 있어야 함
        results["price_fmt"] = results["price"].apply(
            lambda x: f"{int(x):,} 원"
        )

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
