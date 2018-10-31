import json

import requests
from flask import Flask, Response, request, redirect
from flask_cors import CORS

from settings import AUTH_SERVICE_URL, POSTS_SERVICE_URL, PROFILES_SERVICE_URL

app = Flask(__name__)
CORS(app)


@app.route('/register', methods=['POST'])
def register():
    account_data = {
        "email": request.json.get('email'),
        "password": request.json.get('password'),
    }

    response = requests.post(
        AUTH_SERVICE_URL+'/register',
        headers={
            **request.headers,
            'content-type': 'application/json'
        },
        data=json.dumps(account_data),
    )

    if response.status_code == 200:
        profile_data = {
            "user": response.json().get('user')['id'],
            "first_name": request.json.get('first_name'),
            "last_name": request.json.get('last_name'),
        }
        profiles_res = requests.put(
            PROFILES_SERVICE_URL+'/profiles/{user_id}'.format(
                user_id=response.json().get('user')['id']
            ),
            headers={
                'Authorization': 'jwt {}'.format(response.json()['token']),
                'content-type': 'application/json'
            },
            data=json.dumps(profile_data),

        )
        return Response(
            profiles_res.text,
            status=profiles_res.status_code
        )
    return Response(
        response.text,
        status=response.status_code
    )


@app.route('/login', methods=['POST'])
def login():
    response = requests.post(
        AUTH_SERVICE_URL + '/login',
        headers={'content-type': 'application/json'},
        data=request.data  # json.dumps({"email": "test@gmail.com", "password": "dupa"})
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


@app.route('/posts/<post_id>/like', methods=['PUT'])
def like_post(post_id):
    response = requests.put(
        POSTS_SERVICE_URL + f'/posts/{post_id}/like',
        headers=request.headers
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


@app.route('/users/<user_id>', methods=['GET'])
def profile(user_id):
    response = requests.get(
        PROFILES_SERVICE_URL + '/profiles/{}'.format(user_id),
        headers=request.headers,
    )

    return Response(
        response.text,
        status=response.status_code,
        # headers={'content-type': 'application/json'},
    )


@app.route('/users')
def user_list():
    query_params = request.query_string.decode("utf-8")
    url = f"{PROFILES_SERVICE_URL}/profiles?{query_params}"

    response = requests.get(
        url,
        headers=request.headers
    )

    return Response(
        response.text,
        status=response.status_code
    )


@app.route('/media/<id>')
def media(id):
    url = f"{PROFILES_SERVICE_URL}/media/{id}"

    return redirect(url)


if __name__ == '__main__':
    app.run()
