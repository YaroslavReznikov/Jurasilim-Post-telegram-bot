import flask
import telebot
from flask import Flask, request, Response
from setup import bot

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.headers.get("content-type") == 'application/json':
        update = telebot.types.Update.de_json(request.stream.read().decode('UTF-8'))
        bot.process_new_updates(update)
    else:
        flask.abort(403)
    if request.method == 'Post':
        return Response('ok', status=200)
    else:
        return ' '


app.run()
