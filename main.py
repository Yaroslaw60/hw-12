import json

from flask import Flask, render_template, request

app = Flask(__name__)

file_candidate = open("static/candidates.json", encoding="utf-8")
file_settings = open("static/settings.json", encoding="utf-8")

app.config["candidate"] = json.load(file_candidate)
app.config["settings"] = json.load(file_settings)

settings = app.config["settings"]
candidates = app.config["candidate"]


@app.route("/")
def main_page():
    """
    Возвращает на экран статус приложения в зависимости от значения 'online'.
    """
    if settings["online"]:
        return "Приложение работает"
    return "Приложение не работает"


@app.route("/candidate/<int:x>")
def candidate_page(x):
    """
    :param x: ID пользователя введенный в командной строке
    :return: Выводит страницу кандидата по шаблону
    """
    for person in candidates:
        if int(person['id']) == x:
            return render_template("candidat.html", person=person)


@app.route("/list")
def candidate_list():
    return render_template("list_candidates.html", candidates=candidates)


@app.route("/search/")
def search_name():
    """
    Производит поиск по имения и возвращает список с именами кандитатов, а так же ссылки на них
    :return:
    """
    # Если включена эта настройка выполняем поиск без учета регистра.
    if settings['case-sensitive']:
        search = request.args.get("name")
        # создаем список имен найденных пользователей
        list_name = [x["name"] for x in candidates if search in x["name"].lower()]
        len_list = len(list_name)
        return render_template("search_page.html", list_name=list_name, len_list=len_list, candidates=candidates)
    # Если же нет то проверяем только то что ввели в командной строке
    else:
        search = request.args.get("name")
        # создаем список имен найденных пользователей
        list_name = [x["name"] for x in candidates if search in x["name"]]
        len_list = len(list_name)
        return render_template("search_page.html", list_name=list_name, len_list=len_list, candidates=candidates)


@app.route("/skill/")
def search_skill():
    """
    Поиск по нужному нам скиллу у кандидатов, и вывод списка у кого он есть (с ограничением по количеству в зависимости
    от настройки 'limit').
    """
    search = request.args.get("skill")
    # Создаем список кандидатов с нужным скиллом. Разбиваем скилы на сплиты, чтобы проверить по списку. А так же
    # делаем все скиллы пользователей нижнего регистра, чтобы легче искать.
    list_candidates = [x for x in candidates if search in x['skills'].lower().split(", ")]
    limit_view = int(settings["limit"])
    if len(list_candidates) > limit_view:
        # Переменная для вывода количества пользователей, которых нет на странице
        and_more = len(list_candidates) - limit_view
        return render_template("search_skill.html",
                               list_candidates=list_candidates[0:limit_view],
                               limit_view=limit_view,
                               search=search,
                               and_more=and_more)
    return render_template("search_skill.html",
                           list_candidates=list_candidates[0:limit_view],
                           limit_view=limit_view,
                           search=search,
                           and_more=and_more)


app.run(debug=True)
