from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)

def normalize(text):
    return str(text).replace(" ", "").lower()

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_excel("price.xlsx")

    group1_list = sorted(df["group1"].dropna().unique().tolist())

    selected_group1 = request.form.get("group1")
    selected_group2 = request.form.get("group2")
    selected_group3 = request.form.get("group3")

    group2_list = None
    group3_list = None
    group4_list = None
    results = None

    if selected_group1:
        group2_list = sorted(
            df[df["group1"] == selected_group1]["group2"]
            .dropna().unique().tolist()
        )

    if selected_group1 and selected_group2:
        group3_list = sorted(
            df[
                (df["group1"] == selected_group1) &
                (df["group2"] == selected_group2)
            ]["group3"].dropna().unique().tolist()
        )

    if selected_group1 and selected_group2 and selected_group3:
        group4_list = sorted(
            df[
                (df["group1"] == selected_group1) &
                (df["group2"] == selected_group2) &
                (df["group3"] == selected_group3)
            ]["group4"].dropna().unique().tolist()
        )

        results = df[
            (df["group1"] == selected_group1) &
            (df["group2"] == selected_group2) &
            (df["group3"] == selected_group3)
        ]

        results["price_fmt"] = results["price"].apply(
            lambda x: f"{int(x):,} 원"
        )

    return render_template(
        "index.html",
        group1_list=group1_list,
        group2_list=group2_list,
        group3_list=group3_list,
        group4_list=group4_list,
        selected_group1=selected_group1,
        selected_group2=selected_group2,
        selected_group3=selected_group3,
        results=results
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



