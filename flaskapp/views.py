from flask import Flask, jsonify
from flask import render_template, request
from datetime import datetime
from . import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods = ['GET', 'POST'])
def result():
    query = request.args.get('query')
    return render_template("home.html", query = query)