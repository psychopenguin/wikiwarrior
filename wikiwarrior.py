#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, make_response, request
import json
from uuid import uuid4
import redis
import requests
from urllib import unquote
from bs4 import BeautifulSoup

app = Flask(__name__)
config = json.loads(open('wikiwarrior.conf.json').read())
app_name = config['app_name']
redis_host = config['redis']['host']
redis_port = config['redis']['port']
redis_db = config['redis']['db']
session_exp = config['game']['session_expiration']
match_exp = config['game']['match_expiration']
wikipedia = config['game']['wikipedia']
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db) 

def creategame():
	random_page = requests.get(wikipedia+'/wiki/Special:Random').url
	article = random_page.split('/')[-1]
	redis_conn.set('running_match', article, match_exp)

def gamerunning():
	return redis_conn.exists('running_match')

def currentgame():
  if not gamerunning():
    creategame()
  return redis_conn.get('running_match')

def gamename():
  return unquote(currentgame()).decode('utf-8')

def unique_id():
	uid = str(uuid4())
	ua = request.headers.get('User-Agent')
	referer = request.headers.get('Referer')
	clicks = 0
	sessison_data = {'User-Agent': ua, 'Referer': referer, 'Clicks': clicks}
	redis_conn.set(uid, sessison_data, session_exp)
	return uid

def wikicontent(html):
  content = BeautifulSoup(html)
  return content.find('div', {'id': 'content'})

@app.route('/')
def home(): 
	response = make_response(render_template('index.html', app_name=app_name, current_game=gamename()))
	response.set_cookie('game_session', unique_id())
	return response

@app.route('/wiki')
@app.route('/wiki/<article>')
def wiki(article = str(currentgame()) ):
  wikipage = wikipedia + "/wiki/" + article
  content = wikicontent(requests.get(wikipage).text)
  response = make_response(render_template('wiki.html', app_name=app_name, current_game=gamename(), content=content))
  return response

if __name__ == '__main__':
	app.run(debug=True)