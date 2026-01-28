from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# 엑셀 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "price.xlsx")
df = pd.read_excel(EXCEL_PATH).fillna("")

# 가격 포맷
df["price_fmt"] = df["price"].apply(lambda x: f"{int(x):,} 원")

@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    group1_list = sorted(df["group1"].unique())

    selected_group1 = request.form.get("group1", "")
    selected_group2 = request.form.get("group2", "")
    selected_group3 = request.form.get("group3", "")
    selected_group4 = request.form.get("group4", "")

    filtered = df.copy()

    if selected_group1:
        filtered = filtered[filtered["group1"] == selected_group1]

    group2_list = sorted(filtered["group2"].unique()) if selected_group1 else []
    if selected_group2:
        filtered = filtered[filtered["group2"] == selected_group2]

    group3_list = sorted(filtered["group3"].unique()) if selected_group2 else []
    if selected_group3:
        filtered = filtered[filtered["group3"] == selected_group3]

    group4_list = sorted(filtered["group4"].unique()) if selected_group3 else []
    if selected_group4:
        filtered = filtered[filtered["group4"] == selected_group4]

    if request.method == "POST":
        results = filtered

    return render_template(
        "index.html",
        group1_list=group1_list,
        group2_list=group2_list,
        group3_list=group3_list,
        group4_list=group4_list,
        selected_group1=selected_group1,
        selected_group2=selected_group2,
        selected_group3=selected_group3,
        selected_group4=selected_group4,
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)
