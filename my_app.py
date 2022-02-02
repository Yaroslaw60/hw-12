import json
from flask import Flask, render_template, request

app = Flask (__name__)


def open_candidates_file():
    with open("candidates.json", "rt", encoding="utf-8") as fp:
        data = json.load(fp)
        return data

def open_settings_file():
    with open("settings.json", "rt", encoding="utf-8") as file:
        settings = json.load(file)
        return settings


@app.route("/")
def main_page():
    return "Hello world!"


if __name__ == "__main__":
    app.run()
