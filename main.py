from flask import Flask, render_template, request, redirect

app = Flask(__name__)


spisok_zadach = []


@app.route("/")
def index():
    return render_template("index.html", zadachi=spisok_zadach)


@app.route("/add", methods=["POST"])
def add():
    tekst = request.form.get("task")
    if tekst:
        spisok_zadach.append({"tekst": tekst, "sdelano": False})
    return redirect("/")


@app.route("/toggle/<int:number>")
def toggle(number):
    if number < len(spisok_zadach):
        spisok_zadach[number]["sdelano"] = not spisok_zadach[number]["sdelano"]
    return redirect("/")


@app.route("/delete/<int:number>")
def delete(number):
    if number < len(spisok_zadach):
        spisok_zadach.pop(number)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
