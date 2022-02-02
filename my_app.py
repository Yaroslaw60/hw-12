import json
from flask import Flask, render_template, request

app = Flask(__name__)

with open("candidates.json", "rt", encoding="utf-8") as file:
    data = json.load(file)


