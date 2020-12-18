"""This file contains fake data to be used throughout tests."""


import json

user_data_json = json.dumps({
    "avatar": {
        "height": 200,
        "url": "https://www.mycdn/2323g34y34",
        "width": 200
    },
    "bio": "",
    "cover_photo": {
        "height": 400,
        "url": "https://www.mycdn/qwtkqw98",
        "width": 500
    },
    "email": "brad@gmail.com",
    "id": "18feb26ae2d5435d80d8798beb3b3d5d",
    "is_admin": False,
    "joined_on": "2020-12-17T20:11:17.526502",
    "last_seen_at": "2020-12-17T20:11:17.526492",
    "location": {
        "city": "Philadelphia",
        "country": "United States",
        "state": "Pennsylvania"
    },
    "name": "Brad",
    "resource_type": "User",
    "username": "brad345"
})


user_data_dict = {
    "name": "Brad",
    "username": "brad345",
    "email": "brad@gmail.com",
    "password": "facebook",
    "location": {
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "country": "United States"
    }
}