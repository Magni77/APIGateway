import json

import requests
from flask import Flask, Response, request

from settings import AUTH_SERVICE_URL, POSTS_SERVICE_URL

app = Flask(__name__)

# TODO registration API should be POST and have request to profile service with first&last name


@app.route('/register')
def register():
    response = requests.post(
        AUTH_SERVICE_URL+'/register',
        headers={'content-type': 'application/json'},
        data=json.dumps({"email": "test@gmail.com", "password": "dupa"})
    )

    return Response(
        response.text,
        status=response.status_code
    )


@app.route('/login')
def login():
    response = requests.post(
        AUTH_SERVICE_URL + '/login',
        headers={'content-type': 'application/json'},
        data=json.dumps({"email": "test@gmail.com", "password": "dupa"})
    )

    return Response(
        response.text,
        status=response.status_code
    )


@app.route('/accounts')
def accounts():
    response = requests.get(
        AUTH_SERVICE_URL + '/accounts',
        headers=request.headers,
    )
    print(response.text)
    # print(response.json())
    print(response.headers)
    print(response.status_code)
    return Response(
        response.text,
        status=response.status_code,
        # headers={'content-type': 'application/json'},
    )


@app.route('/posts', methods=['POST'])
def create_post():
    response = requests.post(
        POSTS_SERVICE_URL + '/posts',
        headers=request.headers,
        data=request.data
    )

    return Response(
        response.text,
        status=response.status_code
    )


@app.route('/users/<user_id>/posts', methods=['GET'])
def user_posts(user_id):
    response = requests.get(
        POSTS_SERVICE_URL + f'/posts?author_id={user_id}',
        headers=request.headers
    )

    return Response(
        response.text,
        status=response.status_code
    )


if __name__ == '__main__':
    app.run()
