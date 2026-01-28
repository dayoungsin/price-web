from flask import Flask, render_template, request
import pandas as pd
import math

app = Flask(__name__)

def fmt_price(x):
    if pd.isna(x):
        return ""
    return f"{int(x):,} 원"

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_excel("price.xlsx")

    # NaN → 빈 문자열
    df = df.fillna("")

    # 드롭다운용 데이터
    group1_list = sorted(df["group1"].unique())

    selected_group1 = request.form.get("group1", "")
    selected_group2 = request.form.get("group2", "")

    group2_list = []
    results = None

    if selected_group1:
        group2_list = sorted(
            df[df["group1"] == selected_group1]["group2"].unique()
        )

    if selected_group1 or selected_group2:
        results = df.copy()

        if selected_group1:
            results = results[results["group1"] == selected_group1]

        if selected_group2:
            results = results[results["group2"] == selected_group2]

        results["price_fmt"] = results["price"].apply(fmt_price)

    return render_template(
        "index.html",
        group1_list=group1_list,
        group2_list=group2_list,
        results=results,
        selected_group1=selected_group1,
        selected_group2=selected_group2,
    )

if __name__ == "__main__":
    app.run(debug=True)
