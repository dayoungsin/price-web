from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)

def normalize(text):
    return str(text).replace(" ", "").lower()

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_excel("price.xlsx")

    # 🔹 group1 리스트 (항상 생성)
    group1_list = sorted(df["group1"].dropna().unique())

    selected_group1 = None
    results = None

    if request.method == "POST":
        selected_group1 = request.form.get("group1")

        if selected_group1:
            results = df[df["group1"] == selected_group1]

            if not results.empty:
                results["price_fmt"] = results["price"].apply(
                    lambda x: f"{int(x):,} 원"
                )

    return render_template(
        "index.html",
        group1_list=group1_list,
        selected_group1=selected_group1,
        results=results
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


