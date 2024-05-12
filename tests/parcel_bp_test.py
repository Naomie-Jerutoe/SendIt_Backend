import pytest
from flask import json
from models import db, Parcel, User
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    db.session.remove()
    db.drop_all()

def test_create_parcel_order(client):
    # First, we need to create a user
    user = User(username='testuser', password='testpassword', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Then, we log in the user to get the access token
    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    data = json.loads(response.data)
    access_token = data['access_token']

    # Now we can create a parcel order
    response = client.post('/parcels', data=json.dumps({
        'pickup_location': 'Nairobi',
        'destination': 'Mombasa',
        'weight': 10,
        'price': 500,
        'description': 'A small package'
    }), content_type='application/json', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Hooray! Your parcel order has been created successfully!'

    # Check that the parcel was correctly saved to the database
    parcel = Parcel.query.filter_by(user_id=user.id).first()
    assert parcel is not None
    assert parcel.pickup_location == 'Nairobi'
    assert parcel.destination == 'Mombasa'
    assert parcel.weight == 10
    assert parcel.price == 500
    assert parcel.description == 'A small package'

# Second Route 
def test_get_parcel(client):
    # First, we need to create a user
    user = User(username='testuser', password='testpassword', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()

    # log in the user to get the access token
    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    data = json.loads(response.data)
    access_token = data['access_token']

    # create a parcel order
    response = client.post('/parcels', data=json.dumps({
        'pickup_location': 'Nairobi',
        'destination': 'Mombasa',
        'weight': 10,
        'price': 500,
        'description': 'A small package'
    }), content_type='application/json', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Hooray! Your parcel order has been created successfully!'

    # Check that the parcel was correctly saved to the database
    parcel = Parcel.query.filter_by(user_id=user.id).first()
    assert parcel is not None
    assert parcel.pickup_location == 'Nairobi'
    assert parcel.destination == 'Mombasa'
    assert parcel.weight == 10
    assert parcel.price == 500
    assert parcel.description == 'A small package'

    # Now we can get the details of the parcel order
    response = client.get(f'/parcels/{parcel.id}', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Great! We found your parcel details!'
    assert data['parcel'] == parcel.__repr__()

# Third Route 
def test_change_destination(client):
    # First, we need to create a user
    user = User(username='testuser', password='testpassword', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Then, we log in the user to get the access token
    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    data = json.loads(response.data)
    access_token = data['access_token']

    # Now we can create a parcel order
    response = client.post('/parcels', data=json.dumps({
        'pickup_location': 'Nairobi',
        'destination': 'Mombasa',
        'weight': 10,
        'price': 500,
        'description': 'A small package'
    }), content_type='application/json', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Hooray! Your parcel order has been created successfully!'

    # Check that the parcel was correctly saved to the database
    parcel = Parcel.query.filter_by(user_id=user.id).first()
    assert parcel is not None
    assert parcel.pickup_location == 'Nairobi'
    assert parcel.destination == 'Mombasa'
    assert parcel.weight == 10
    assert parcel.price == 500
    assert parcel.description == 'A small package'

    # Now we can change the destination of the parcel order
    new_destination = 'Kisumu'
    response = client.put(f'/parcels/{parcel.id}/destination', data=json.dumps({
        'destination': new_destination
    }), content_type='application/json', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Destination updated successfully! Your parcel is on its way to the new destination.'
    assert data['parcel']['destination'] == new_destination

    # Check that the parcel's destination was correctly updated in the database
    parcel = Parcel.query.get(parcel.id)
    assert parcel.destination == new_destination

# Third Route 
def test_cancel_parcel(client):
    # First, we need to create a user
    user = User(username='testuser', password='testpassword', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Then, we log in the user to get the access token
    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    data = json.loads(response.data)
    access_token = data['access_token']

    # Now we can create a parcel order
    response = client.post('/parcels', data=json.dumps({
        'pickup_location': 'Nairobi',
        'destination': 'Mombasa',
        'weight': 10,
        'price': 500,
        'description': 'A small package'
    }), content_type='application/json', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Hooray! Your parcel order has been created successfully!'

    # Check that the parcel was correctly saved to the database
    parcel = Parcel.query.filter_by(user_id=user.id).first()
    assert parcel is not None
    assert parcel.pickup_location == 'Nairobi'
    assert parcel.destination == 'Mombasa'
    assert parcel.weight == 10
    assert parcel.price == 500
    assert parcel.description == 'A small package'

    # Now we can cancel the parcel order
    response = client.post(f'/parcels/{parcel.id}/cancel', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Parcel cancelled successfully! We\'ve halted delivery for this parcel.'
    assert data['parcel']['status'] == 'cancelled'

    # Check that the parcel's status was correctly updated in the database
    parcel = Parcel.query.get(parcel.id)
    assert parcel.status == 'cancelled'

# Fifth Route
def test_get_user_parcels(client):
    # First, we need to create a user
    user = User(username='testuser', password='testpassword', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Then, we log in the user to get the access token
    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    data = json.loads(response.data)
    access_token = data['access_token']

    # Now we can create a few parcel orders
    for i in range(3):
        response = client.post('/parcels', data=json.dumps({
            'pickup_location': 'Nairobi',
            'destination': 'Mombasa',
            'weight': 10,
            'price': 500,
            'description': f'A small package {i}'
        }), content_type='application/json', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert response.status_code == 201

    # Now we can get the list of all parcel deliveries associated with the user
    response = client.get(f'/users/{user.id}/parcels', headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check that the request was successful
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Here are all the parcels associated with this user!'
    assert len(data['parcels']) == 3

    # Check that the parcels were correctly retrieved from the database
    parcels = Parcel.query.filter_by(user_id=user.id).all()
    for i, parcel in enumerate(parcels):
        assert parcel.__repr__() == data['parcels'][i]
