try:
    import requests

    response = requests.get('http://localhost:5000/users')

    assert response.status_code == 200
    assert response.json() == [
        {
            "email": "sivel123@email.com",
            "id": 6,
            "is_admin": True,
            "username": "sivel123"
        },
        {
            "email": "Johnsivel@email.com",
            "id": 7,
            "is_admin": True,
            "username": "oscar"
        },
        {
            "email": "jamesdavid@email.com",
            "id": 8,
            "is_admin": True,
            "username": "davidjames"
        },
        {
            "email": "jonathan@gmail.com",
            "id": 9,
            "is_admin": True,
            "username": "Jonathan Kim"
        },
        {
            "email": "davioscar@email.com",
            "id": 11,
            "is_admin": False,
            "username": "muchiri"
        },
        {
            "email": "felista@email.com",
            "id": 13,
            "is_admin": True,
            "username": "felista"
        },
        {
            "email": "george@email.com",
            "id": 12,
            "is_admin": True,
            "username": "george"
        },
        {
            "email": "levis@gmail.com",
            "id": 14,
            "is_admin": False,
            "username": "Levis Ngigi"
        },
        {
            "email": "dennis@gmail.com",
            "id": 16,
            "is_admin": False,
            "username": "Dennis Ngigi"
        },
        {
            "email": "naomi@gmail.com",
            "id": 17,
            "is_admin": True,
            "username": "Naomie Jeruto"
        },
        {
            "email": "collins@gmail.com",
            "id": 18,
            "is_admin": False,
            "username": "Collins Bett"
        },
        {
            "email": "jane@gmail.com",
            "id": 19,
            "is_admin": False,
            "username": "Jane Doe"
        },
        {
            "email": "brian@gmail.com",
            "id": 20,
            "is_admin": True,
            "username": "brian"
        },
        {
            "email": "johnkip@gmail.com",
            "id": 23,
            "is_admin": True,
            "username": "John Kip"
        },
        {
            "email": "naomicherutolagat@gmail.com",
            "id": 24,
            "is_admin": False,
            "username": "naomi lagat"
        },
        {
            "email": "john@example.com",
            "id": 1,
            "is_admin": True,
            "username": "Johndoe"
        },
        {
            "email": "joe@gmail.com",
            "id": 25,
            "is_admin": True,
            "username": "joe"
        },
        {
            "email": "kipkirui@gmail.com",
            "id": 26,
            "is_admin": False,
            "username": "kipkirui"
        },
        {
            "email": "kip@gmail.com",
            "id": 27,
            "is_admin": True,
            "username": "kip"
        },
        {
            "email": "max@gmail.com",
            "id": 28,
            "is_admin": True,
            "username": "max"
        },
        {
            "email": "mat@gmail.com",
            "id": 32,
            "is_admin": True,
            "username": "mat"
        },
        {
            "email": "bryo@gmail.com",
            "id": 34,
            "is_admin": True,
            "username": "bryo"
        },
        {
            "email": "bryokm@gmail.com",
            "id": 35,
            "is_admin": False,
            "username": "Brian K"
        },
        {
            "email": "sirbryo@gmail.com",
            "id": 37,
            "is_admin": True,
            "username": "sirbryo"
        },
        {
            "email": "John@email.com",
            "id": 5,
            "is_admin": False,
            "username": "davidjohn"
        }
    ]
    print('-----------------------------------GOT ALL USERS SUCCESSFULLY-----------------------------------------')
except Exception:
    print("-------------------------------------GETTING ALL USERS FAILED-----------------------------")

try:
    import requests
    user_id = 5 
    response = requests.get(f'http://localhost:5000/users/{user_id}')

    assert response.status_code == 200
    assert response.json() == {
            "email": "John@email.com",
            "id": 5,
            "is_admin": False,
            "username": "davidjohn"
        }
    print('-----------------------------------GOT USER 5 SUCCESSFULLY-----------------------------------------')
except Exception:
    print("-------------------------------------GETTING USER 5 FAILED-----------------------------")

try:
    import requests
    user_id = 5  
    data = {'username': 'davidjohn'}
    response = requests.patch(f'http://localhost:5000/users/{user_id}', json=data)

    assert response.status_code == 201
    assert response.json() == {
        "email": "John@email.com",
        "id": 5,
        "is_admin": False,
        "username": "davidjohn"
    }
    print("-------------------------------------UPDATED USER 5 SUCCESSFULLY-----------------------------")
except Exception:
    print("-------------------------------------UPDATING USER 5 FAILED-----------------------------")   

try:
    import requests
    user_id = 37  
    response = requests.delete(f'http://localhost:5000/users/{user_id}')

    assert response.status_code == 200
    assert response.json() == { "Message": "User deleted"}
    print("-------------------------------------DELETED USER 37 SUCCESSFULLY-----------------------------")
except Exception:
    print("-------------------------------------DELETING USER 37 FAILED-----------------------------")