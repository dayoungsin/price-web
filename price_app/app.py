from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("price.xlsx").fillna("")

@app.route("/", methods=["GET", "POST"])
def index():
    selected_group1 = request.form.get("group1", "")
    selected_group2 = request.form.get("group2", "")
    selected_group3 = request.form.get("group3", "")
    selected_group4 = request.form.get("group4", "")

    # group1 목록
    group1_list = sorted(df["group1"].unique())

    # group2
    group2_list = []
    if selected_group1:
        group2_list = sorted(
            df[df["group1"] == selected_group1]["group2"].unique()
        )

    # group3
    group3_list = []
    if selected_group2:
        group3_list = sorted(
            df[
                (df["group1"] == selected_group1) &
                (df["group2"] == selected_group2)
            ]["group3"].unique()
        )
        group3_list = [g for g in group3_list if g != ""]

    # group4
    group4_list = []
    if selected_group3:
        group4_list = sorted(
            df[
                (df["group1"] == selected_group1) &
                (df["group2"] == selected_group2) &
                (df["group3"] == selected_group3)
            ]["group4"].unique()
        )
        group4_list = [g for g in group4_list if g != ""]

    # 결과 필터링
    results = df.copy()
    if selected_group1:
        results = results[results["group1"] == selected_group1]
    if selected_group2:
        results = results[results["group2"] == selected_group2]
    if selected_group3:
        results = results[results["group3"] == selected_group3]
    if selected_group4:
        results = results[results["group4"] == selected_group4]

    if not results.empty:
        results["price_fmt"] = results["price"].apply(lambda x: f"{int(x):,} 원")

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

