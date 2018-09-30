from flask import Flask, jsonify
from flask import render_template
from datetime import datetime
from . import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api?query=<query>")
def get_papers(query):
    return jsonify({'result': query})