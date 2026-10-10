from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sekret"


def spisok():
    if "zadachi" not in session:
        session["zadachi"] = []
    return session["zadachi"]


@app.route("/")
def index():
    vse = spisok()
    filtr = request.args.get("filtr", "vse")
    kat = request.args.get("kat", "")

    otobrazhenie = []
    for i, z in enumerate(vse):
        if filtr == "aktivnye" and z["sdelano"]:
            continue
        if filtr == "vypolnennye" and not z["sdelano"]:
            continue
        if filtr == "segodnya" and z["data"] != datetime.now().strftime("%Y-%m-%d"):
            continue
        if kat and z["kategoriya"] != kat:
            continue
        otobrazhenie.append({"nomer": i, **z})

    otobrazhenie.sort(key=lambda z: z["sdelano"])
    kategorii = sorted({z["kategoriya"] for z in vse if z["kategoriya"]})

    return render_template("index.html", zadachi=otobrazhenie,
                           filtr=filtr, kat=kat, kategorii=kategorii)


@app.route("/add", methods=["POST"])
def add():
    tekst = request.form.get("task")
    if tekst:
        vse = spisok()
        vse.append({
            "tekst": tekst,
            "sdelano": False,
            "kategoriya": request.form.get("kategoriya", "").strip(),
            "data": datetime.now().strftime("%Y-%m-%d"),
        })
        session["zadachi"] = vse
    return redirect("/")


@app.route("/toggle/<int:n>")
def toggle(n):
    vse = spisok()
    if n < len(vse):
        vse[n]["sdelano"] = not vse[n]["sdelano"]
        session["zadachi"] = vse
    return redirect("/")


@app.route("/delete/<int:n>")
def delete(n):
    vse = spisok()
    if n < len(vse):
        vse.pop(n)
        session["zadachi"] = vse
    return redirect("/")


@app.route("/edit/<int:n>", methods=["POST"])
def edit(n):
    vse = spisok()
    if n < len(vse) and request.form.get("task"):
        vse[n]["tekst"] = request.form.get("task")
        vse[n]["kategoriya"] = request.form.get("kategoriya", "").strip()
        session["zadachi"] = vse
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
