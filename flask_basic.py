#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, g, signals, Blueprint
import yaml
from flask.signals import signals_available

if not signals_available:
    raise RuntimeError("pip install blinker")

app = Flask(__name__)
teams = Blueprint('teams', __name__)

_DEVS = ['Joe', 'Da', 'Quebrada']
_OPS = ['Outro', 'Joe']
_TEAMS = {1: _DEVS, 2: _OPS}

@teams.route('/teams')
def get_all():
    return jsonify(_TEAMS)

@teams.route('/teams/<int:team_d>')
def get_team(team_id):
    return jsonify(_TEAMS[team_id])

def finished(sender, response, **extra):
    print("About to send a Response")
    print(response)

signals.request_finished.connect(finished)

@app.before_request
def authenticate():
    if request.authorization:
        g.user = request.authorization['username']
    else:
        g.user = 'Anonymous'

@app.route("/")
def auth():
    print("The raw Authorization header")
    print(request.environ["HTTP_AUTHORIZATION"])
    print("Flask's Authorization header")
    print(request.authorization)
    return ""

@app.route('/api/')
def my_microservice(): 
    print(request) 
    print(request.environ) 
    response = jsonify({'Hello': 'World!'}) 
    print(response) 
    print(response.data) 
    return response 

@app.route('/api/person/<person_id>')
def person(person_id):
    response = jsonify({'Hello': person_id})
    return response

@app.route('/api/yaml')
def yaml_test():
    response = yamlify("Tretas Pesadas")
    return response

def yamlify(data, status=200, headers=None):
    _headers = {'Content-Type':'application/x-yaml'}
    if headers is not None:
        _headers.update(headers)
    return yaml.safe_dump(data), status, _headers

if __name__ == '__main__': 
    print(app.url_map) 
    app.run() 
