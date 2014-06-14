#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, make_response, request
import json
from uuid import uuid4

def unique_id():
	uid = str(uuid4())
	return uid

config = json.loads(open('wikiwarrior.conf.json').read())
app = Flask(__name__)

app_name = config['app_name']


@app.route('/')
def home():
  response = make_response(render_template('index.html', app_name=app_name))
  response.set_cookie('game_session', unique_id())
  return response

if __name__ == '__main__':
        app.run(debug=True)