# Flask
from flask import Flask, url_for, request, render_template, jsonify


@app.route('/')
def index():
    return {"hello" : "world"}