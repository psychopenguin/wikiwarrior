from flask import Flask, render_template, make_response, request
import json

config = json.loads(open('wikiwarrior.conf.json').read())
app = Flask(__name__)

app_name = config['app_name']


@app.route('/')
def home():
  response = make_response(render_template('index.html', app_name=app_name))
  return response

if __name__ == '__main__':
        app.run(debug=True)