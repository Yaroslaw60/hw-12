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


@app.route("/search/")
def search_name():
    settings = open_settings_file()
    candidates = open_candidates_file()
    if settings['case-sensitive']:
        search = request.args.get("name")
        list_name = [x["name"] for x in candidates if search in x["name"].lower()]
        len_list = len(list_name)
        return render_template("search_page.html", list_name=list_name, len_list=len_list, candidates=candidates)
    else:
        search = request.args.get("name")
        list_name = [x["name"] for x in candidates if search in x["name"]]
        len_list = len(list_name)
        return render_template("search_page.html", list_name=list_name, len_list=len_list, candidates=candidates)


@app.route("/skill/")
def search_skill():
    candidates = open_candidates_file()
    settings = open_settings_file()
    search = request.args.get("skill")
    list_candidates = [x for x in candidates if search in x['skills'].lower().split(", ")]
    limit_view = int(settings["limit"])
    if len(list_candidates) > limit_view:
        and_more = len(list_candidates) - limit_view
        return render_template("search_skill.html",
                               list_candidates=list_candidates[0:limit_view],
                               limit_view=limit_view,
                               search=search,
                               and_more=and_more)
    else:
        return render_template("search_skill.html",
                               list_candidates=list_candidates[0:limit_view],
                               limit_view=limit_view,
                               search=search,
                               )






app.run(debug=True)
