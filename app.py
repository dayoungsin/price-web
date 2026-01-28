from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_excel("price.xlsx")

    group1_list = sorted(df["group1"].dropna().unique())

    selected_group1 = request.form.get("group1")
    group2_list = []

    if selected_group1:
        group2_list = sorted(
            df[df["group1"] == selected_group1]["group2"]
            .dropna()
            .unique()
        )

    return render_template(
        "index.html",
        group1_list=group1_list,
        group2_list=group2_list,
        selected_group1=selected_group1
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
