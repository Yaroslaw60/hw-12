from flask import Flask, render_template, request
import json
app = Flask(__name__)


def open_candidates_file():
    with open("static/candidates.json", "rt", encoding="utf-8") as fp:
        data = json.load(fp)
        return data

def open_settings_file():
    with open("static/settings.json", "rt", encoding="utf-8") as file:
        settings = json.load(file)
        return settings


@app.route("/")
def main_page():
    settings = open_settings_file()
    if settings["online"]:
        return "Приложение работает"
    else:
        return "Приложение не работает"

@app.route("/candidate/<int:x>")
def candidate_page(x):
    candidates = open_candidates_file()
    for person in candidates:
        if int(person['id']) == x:
            return render_template("candidat.html", person=person)
            break
        else:
            continue

@app.route("/list")
def candidate_list():
    candidates = open_candidates_file()
    return render_template("list_candidates.html", candidates=candidates)


@app.route("/search")



app.run(debug=True)