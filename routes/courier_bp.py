from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from flask_jwt_extended import jwt_required, get_jwt
from schemas import profileSchema
import cloudinary
import cloudinary.utils
import cloudinary.uploader

from auth_middleware import admin_required
from models import db, Profile, User

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
    user_claims = get_jwt()
    user_id = user_claims['sub'].get('userId')
    
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

class RemoveProfilePicture(Resource):
    @jwt_required()
    def delete(self):
        user_claims = get_jwt()
        user_id = user_claims['sub'].get('userId')

        try:
            profile = Profile.query.filter_by(user_id=user_id).first()

            if profile:
                # Check if the profile picture exists
                if profile.profile_picture:
                    # # Delete the image from Cloudinary
                    public_id = profile.profile_picture.split('/')[-1].split('.')[0]
                    cloudinary.uploader.destroy(public_id)

                    # Remove the profile picture URL from the database
                    profile.profile_picture = None
                    db.session.commit()

                    return make_response(jsonify({'message': 'Profile picture removed successfully.'}), 200)
                else:
                    return make_response(jsonify({"error": "Profile picture not found"}), 404)
            else:
                return make_response(jsonify({"error": "Profile not found"}), 404)
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(RemoveProfilePicture, '/remove_profile_picture')

class UpdateProfile(Resource):
    @jwt_required()
    def put(self):
        user_claims = get_jwt()
        user_id = user_claims['sub'].get('userId')

        # Get the updated profile information from the request
        updated_data = request.json
        
        try:
            profile = Profile.query.filter_by(user_id=user_id).first()

            if profile:
                # Update the profile fields with the new information
                if 'profile_picture' in updated_data:
                    profile.profile_picture = updated_data['profile_picture']
                if 'location' in updated_data:
                    profile.location = updated_data['location']
                
                # Commit the changes to the database
                db.session.commit()
                
                return make_response(jsonify({'message': 'Profile updated successfully'}), 200)
            else:
                return make_response(jsonify({"error": "Profile not found"}), 404)
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(UpdateProfile, '/update_profile')

