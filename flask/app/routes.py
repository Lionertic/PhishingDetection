# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app

@app.route('/')
@app.route('/index')
def index():
    map = {}
    map['message'] = 'hii'
    return jsonify(map)

@app.route('/about')
def about():
    return jsonify(render_template('about.html'))




