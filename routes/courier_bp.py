from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource, abort
from flask_marshmallow import Marshmallow
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas import profileSchema
import cloudinary
import cloudinary.uploader

from auth_middleware import admin_required
from models import db, Profile

profile_bp = Blueprint('profile_bp', __name__)
ma = Marshmallow(profile_bp)
api = Api(profile_bp)

class UserProfile(Resource):
  @admin_required
  def get(self):
    profiles = Profile.query.all()
    result = profileSchema.dump(profiles, many=True)
    response = make_response(jsonify(result), 200)

    return response
api.add_resource(UserProfile, '/profiles')
  
class UploadProfilePicture(Resource):
  @jwt_required()
  def post(self):
    user_id = get_jwt_identity()
    
    if 'profile_photo' not in request.files:
      return make_response(jsonify({"error": "No picture provided"}))
    
    profile_photo = request.files['profile_photo']
    
    if profile_photo.filename == "":
      return make_response(jsonify({"message":"No profile picture selected"}), 400)
    
    try:
      if profile_photo:
        upload_result = cloudinary.uploader.upload(profile_photo)
        photo_url = upload_result.get('secure_url')
        
        profile = Profile.query.filter_by(user_id=user_id).first()
        
        if profile:
        # Update the existing profile
          profile.profile_picture = photo_url
          
        else:
        # Create a new profile
            new_profile = Profile(
                user_id=user_id,
                profile_picture=photo_url,
                location=request.form.get('location')
            )
            db.session.add(new_profile)

            db.session.commit()
        
        return make_response(jsonify({"message": "profile picture uploaded successfully", "photo_url": photo_url, "result": upload_result}))
      
      else:
        photo_url = None
      
    except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(UploadProfilePicture, '/upload_profile_picture')