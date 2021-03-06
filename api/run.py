import os
from flask import Flask, Blueprint
from flask_restplus import Api, fields
from flask_jwt_extended import JWTManager
from .schema import create_tables

from .views import auth, ride, request
from .models import token_model

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = "superpower"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(app,
          authorizations=authorizations,
          security='apiKey',
          description='Star Ride API endpoint'
          )


@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    jti = decrypted_token['jti']
    return token_model.Token.is_revoked(jti)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


create_tables()

"""Register user"""

user_namespace = api.namespace(
    "Users API", description="User registration APIs", path="/api/v1/auth")
user_namespace.add_resource(auth.Register, "/signup")
user_namespace.add_resource(auth.Login, "/login")
user_namespace.add_resource(auth.Logout, "/logout")

ride_namespace = api.namespace(
    "Rides API", description="Ride APIs", path="/api/v1/rides")
ride_namespace.add_resource(ride.Ride, "/create")
ride_namespace.add_resource(ride.Ride, "/")
ride_namespace.add_resource(ride.RideDetails, "/<ride_id>")
ride_namespace.add_resource(ride.CompleteRide, "/<ride_id>/complete")

request_namespace = api.namespace(
    "Requests API", description="Request APIs", path="/api/v1/rides")
request_namespace.add_resource(request.RideRequest, "/<ride_id>/book")
request_namespace.add_resource(request.ProcessRequest, "/<ride_id>/requests")
request_namespace.add_resource(
    request.ProcessRequest, "/<ride_id>/requests/<request_id>")
request_namespace.add_resource(
    request.RidePassengers, "/<ride_id>/passengers")

request_namespace.add_resource(
    request.RidePassenger, "/<ride_id>/passengers/<passenger_id>")
