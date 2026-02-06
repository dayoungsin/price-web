@app.route("/api/groups", methods=["POST"])
def api_groups():
    df = pd.read_excel("price.xlsx")
    payload = request.get_json() or {}

    g1 = payload.get("group1")
    g2 = payload.get("group2")
    g3 = payload.get("group3")

    result = {}

    if g1:
        result["group2"] = sorted(
            df[df["group1"] == g1]["group2"]
            .dropna().unique().tolist()
        )

    if g1 and g2:
        result["group3"] = sorted(
            df[
                (df["group1"] == g1) &
                (df["group2"] == g2)
            ]["group3"].dropna().unique().tolist()
        )

    if g1 and g2 and g3:
        result["group4"] = sorted(
            df[
                (df["group1"] == g1) &
                (df["group2"] == g2) &
                (df["group3"] == g3)
            ]["group4"].dropna().unique().tolist()
        )

    return jsonify(result)
