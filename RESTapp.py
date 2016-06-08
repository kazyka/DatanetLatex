#!/usr/bin/env python

from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)

todo = [
  {
    'id': 1,
    'text': u'My Note',
    'completed': False
  },
  {
    'id': 2,
    'text': u'Learn to play',
    'completed': False
  }
]


@app.errorhandler(400)
def not_found(error):
  return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'ID not found'}), 404)


@app.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
  tmptodo = [tmptodo for tmptodo in todo if tmptodo['id'] == todo_id]
  if len(tmptodo) == 0:
      abort(404)
  return jsonify({'tmptodo': tmptodo[0]})


@app.route('/todo/', methods=['GET'])
def index():
  return jsonify({'todo': todo})


@app.route('/todo/', methods=['POST'])
def create_todo():
  if not request.json or not 'text' in request.json:
      abort(400)
  tmptodo = {
    'id': todo[-1]['id'] + 1,
    'text': request.json['text'],
    'completed': False
  }
  todo.append(tmptodo)
  return jsonify({'tmptodo', tmptodo}), 201


@app.route('/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
  tmptodo = [tmptodo for tmptodo in todo if tmptodo['id'] == todo_id]
  if len(tmptodo) == 0:
      abort(404)
  if not request.json:
      abort(400)
  if 'text' in request.json and type(request.json['text']) != unicode:
      abort(400)
  if 'completed' in request.json and type(request.json['completed']) is not bool:
      abort(400)
  tmptodo[0]['text'] = request.json.get('text', tmptodo[0]['text'])
  tmptodo[0]['completed'] = request.json.get('completed', tmptodo[0]['completed'])
  return jsonify({'tmptodo': tmptodo[0]})


@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  tmptodo = [tmptodo for tmptodo in todo if tmptodo['id'] == todo_id]
  if len(tmptodo) == 0:
      abort(404)
  todo.remove(tmptodo[0])
  return jsonify({'result': True})

if __name__ == '__main__':
  app.run(debug=True)


