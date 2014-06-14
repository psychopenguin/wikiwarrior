#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, make_response, request
import json
from uuid import uuid4
import redis

app = Flask(__name__)
config = json.loads(open('wikiwarrior.conf.json').read())
app_name = config['app_name']
redis_host = config['redis']['host']
redis_port = config['redis']['port']
redis_db = config['redis']['db']
session_exp = config['game']['expiration']
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db) 

def unique_id():
	uid = str(uuid4())
	ua = request.headers.get('User-Agent')
	referer = request.headers.get('Referer')
	clicks = 0
	sessison_data = {'User-Agent': ua, 'Referer': referer, 'Clicks': clicks}
	redis_conn.set(uid, sessison_data, session_exp)
	return uid




@app.route('/')
def home():
  response = make_response(render_template('index.html', app_name=app_name))
  response.set_cookie('game_session', unique_id())
  return response

if __name__ == '__main__':
        app.run(debug=True)