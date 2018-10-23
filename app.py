import json

import requests
from flask import Flask, Response, request
from flask_cors import CORS

from settings import AUTH_SERVICE_URL, POSTS_SERVICE_URL, PROFILES_SERVICE_URL

app = Flask(__name__)
CORS(app)

# TODO registration API should be POST and have request to profile service with first&last name


@app.route('/register', methods=['POST'])
def register():
    print('headers', dict(request.headers))
    account_data = {
        "email": request.json.get('email'),
        "password": request.json.get('password'),
    }
    profile_data = {
        "first_name": request.json.get('fname'),
        "last_name": request.json.get('lname'),
    }
    response = requests.post(
        AUTH_SERVICE_URL+'/register',
        headers={
            **request.headers,
            'content-type': 'application/json'
        },
        data=json.dumps(account_data),
        # headers={'content-type': 'application/json'},
        # data=json.dumps({"email": "test@gmail.com", "password": "dupa"})
    )
    # if response.status_code == 200:
    #     profile_data = {
    #         "user": response.json()['id'],
    #         "first_name": request.json.get('fname'),
    #         "last_name": request.json.get('lname'),
    #     }
    #     profiles_res = requests.put(
    #         PROFILES_SERVICE_URL+'/profiles/{user_id}'.format(
    #             user_id=response.json()['id']
    #         ),
    #         headers={
    #             **request.headers,
    #             'content-type': 'application/json'
    #         },
    #         data=json.dumps(profile_data),
    #
    #     )
    #     return Response(
    #         profiles_res.text,
    #
    #         status=profiles_res.status_code
    #     )
    return Response(
        response.text,
        # headers={
        #     **response.headers,
        # },
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


if __name__ == '__main__':
    app.run()
