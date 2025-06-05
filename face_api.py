# # face_api.py
# from flask import Flask, request, jsonify
# import face_recognition
# import numpy as np
# import os
# import cloudinary
# import cloudinary.uploader
# from pymongo import MongoClient

# app = Flask(__name__)

# # Configure Cloudinary
# cloudinary.config(
#     cloud_name=os.getenv('CLOUDINARY_NAME'),
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )

# # Connect to MongoDB
# client = MongoClient(os.getenv('MONGODB_URI'))
# db = client.attendance_db
# employees = db.employees

# @app.route('/recognize', methods=['POST'])
# def recognize_face():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image provided"}), 400

#     image_file = request.files['image']

#     # Upload to Cloudinary
#     result = cloudinary.uploader.upload(image_file)
#     image_url = result['secure_url']

#     # Load image
#     image = face_recognition.load_image_file(image_file)
#     face_encodings = face_recognition.face_encodings(image)

#     if not face_encodings:
#         return jsonify({"error": "No faces detected"}), 400

#     # Get all employees from DB
#     all_employees = list(employees.find({}, {'image': 1, 'name': 1}))

#     known_face_encodings = []
#     known_face_names = []

#     for emp in all_employees:
#         if 'image' in emp:
#             try:
#                 emp_image = face_recognition.load_image_file(emp['image'])
#                 emp_encoding = face_recognition.face_encodings(emp_image)[0]
#                 known_face_encodings.append(emp_encoding)
#                 known_face_names.append(emp['name'])
#             except:
#                 continue

#     # Compare faces
#     matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
#     name = "Unknown"

#     if True in matches:
#         first_match_index = matches.index(True)
#         name = known_face_names[first_match_index]

#     return jsonify({
#         "employee_name": name,
#         "image_url": image_url
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
# 2
# from flask import Flask, request, jsonify
# import face_recognition
# import numpy as np
# import os
# import cloudinary
# import cloudinary.uploader
# from pymongo import MongoClient
# import logging

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# # Increase max content length
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# cloudinary.config(
#     cloud_name="dctocnh6f",
#     api_key="431511637411541",
#     api_secret="kcLSVrrlB-1ZrsfdJvG7LDnV4xM",
#     # cloud_name=os.getenv("CLOUDINARY_NAME"),
#     # api_key=os.getenv("CLOUDINARY_API_KEY"),
#     # api_secret=os.getenv("CLOUDINARY_API_SECRET"),
# )

# client = MongoClient(os.getenv("MONGODB_URI"))
# db = client.attendance_db
# employees = db.employees


# @app.route("/recognize", methods=["POST"])
# def recognize_face():
#     logging.debug("Received request to /recognize")
#     if "image" not in request.files:
#         logging.error("No image provided in request")
#         return jsonify({"error": "No image provided"}), 400

#     image_file = request.files["image"]
#     logging.debug(f"Received image: {image_file.filename}")

#     try:
#         # Upload to Cloudinary
#         result = cloudinary.uploader.upload(image_file)
#         image_url = result["secure_url"]
#         logging.debug(f"Uploaded to Cloudinary: {image_url}")

#         # Reset file pointer after Cloudinary upload
#         image_file.seek(0)

#         # Load image for face recognition
#         image = face_recognition.load_image_file(image_file)
#         face_encodings = face_recognition.face_encodings(image)

#         if not face_encodings:
#             logging.error("No faces detected in image")
#             return jsonify({"error": "No faces detected"}), 400

#         # Get all employees from DB
#         all_employees = list(employees.find({}, {"_id": 1, "image": 1, "name": 1}))
#         logging.debug(f"Found {len(all_employees)} employees in database")

#         known_face_encodings = []
#         known_face_names = []
#         known_employee_ids = []

#         for emp in all_employees:
#             if "image" in emp:
#                 try:
#                     # Assume emp['image'] is a Cloudinary URL
#                     import requests
#                     from io import BytesIO

#                     response = requests.get(emp["image"])
#                     emp_image = face_recognition.load_image_file(
#                         BytesIO(response.content)
#                     )
#                     emp_encoding = face_recognition.face_encodings(emp_image)
#                     if emp_encoding:
#                         known_face_encodings.append(emp_encoding[0])
#                         known_face_names.append(emp["name"])
#                         known_employee_ids.append(str(emp["_id"]))
#                 except Exception as e:
#                     logging.error(
#                         f"Error processing employee {emp.get('name', 'unknown')}: {e}"
#                     )
#                     continue

#         # Compare faces
#         matches = face_recognition.compare_faces(
#             known_face_encodings, face_encodings[0]
#         )
#         name = "Unknown"
#         employee_id = None

#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_face_names[first_match_index]
#             employee_id = known_employee_ids[first_match_index]
#             logging.debug(f"Match found: {name}, ID: {employee_id}")

#         return jsonify(
#             {"employee_name": name, "employee_id": employee_id, "image_url": image_url}
#         )
#     except Exception as e:
#         logging.error(f"Error in face recognition: {e}")
#         return jsonify({"error": "Face recognition failed"}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
# 2
# from flask import Flask, request, jsonify
# import face_recognition
# import numpy as np
# import os
# import cloudinary
# import cloudinary.uploader
# from pymongo import MongoClient
# import logging
# from dotenv import load_dotenv

# app = Flask(__name__)

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# # Increase max content length
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# # Validate Cloudinary configuration
# cloudinary_name = os.getenv("CLOUDINARY_NAME")
# cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
# cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")

# if not all([cloudinary_name, cloudinary_api_key, cloudinary_api_secret]):
#     logging.error("Missing Cloudinary credentials. Please check .env file.")
#     raise ValueError("Missing Cloudinary credentials. Please check .env file.")

# cloudinary.config(
#     cloud_name=cloudinary_name,
#     api_key=cloudinary_api_key,
#     api_secret=cloudinary_api_secret,
# )

# # Validate MongoDB connection
# mongodb_uri = os.getenv("MONGODB_URI")
# if not mongodb_uri:
#     logging.error("Missing MONGODB_URI. Please check .env file.")
#     raise ValueError("Missing MONGODB_URI. Please check .env file.")

# try:
#     client = MongoClient(mongodb_uri)
#     db = client.FaceGate  # Change from attendance_db to FaceGate
#     employees = db.employees
#     # Test connection
#     client.server_info()
#     logging.info("MongoDB connection successful.")
# except Exception as e:
#     logging.error(f"Failed to connect to MongoDB: {e}")
#     raise


# @app.route("/recognize", methods=["POST"])
# def recognize_face():
#     logging.debug("Received request to /recognize")
#     if "image" not in request.files:
#         logging.error("No image provided in request")
#         return jsonify({"error": "No image provided"}), 400

#     image_file = request.files["image"]
#     logging.debug(f"Received image: {image_file.filename}")

#     try:
#         # Upload to Cloudinary
#         result = cloudinary.uploader.upload(image_file)
#         image_url = result["secure_url"]
#         logging.debug(f"Uploaded to Cloudinary: {image_url}")

#         # Reset file pointer after Cloudinary upload
#         image_file.seek(0)

#         # Load image for face recognition
#         image = face_recognition.load_image_file(image_file)
#         face_encodings = face_recognition.face_encodings(image)

#         if not face_encodings:
#             logging.error("No faces detected in image")
#             return jsonify({"error": "No faces detected"}), 400

#         # Get all employees from DB
#         all_employees = list(employees.find({}, {"_id": 1, "image": 1, "name": 1}))
#         logging.debug(f"Found {len(all_employees)} employees in database")

#         if not all_employees:
#             logging.warning("No employees found in database")
#             return jsonify(
#                 {
#                     "employee_name": "Unknown",
#                     "employee_id": None,
#                     "image_url": image_url,
#                 }
#             )

#         known_face_encodings = []
#         known_face_names = []
#         known_employee_ids = []

#         for emp in all_employees:
#             if "image" in emp:
#                 try:
#                     # Assume emp['image'] is a Cloudinary URL
#                     import requests
#                     from io import BytesIO

#                     response = requests.get(emp["image"])
#                     response.raise_for_status()  # Raise error for bad status
#                     emp_image = face_recognition.load_image_file(
#                         BytesIO(response.content)
#                     )
#                     emp_encoding = face_recognition.face_encodings(emp_image)
#                     if emp_encoding:
#                         known_face_encodings.append(emp_encoding[0])
#                         known_face_names.append(emp["name"])
#                         known_employee_ids.append(str(emp["_id"]))
#                     else:
#                         logging.warning(
#                             f"No face encoding found for employee {emp.get('name', 'unknown')}"
#                         )
#                 except Exception as e:
#                     logging.error(
#                         f"Error processing employee {emp.get('name', 'unknown')}: {e}"
#                     )
#                     continue

#         if not known_face_encodings:
#             logging.warning("No valid face encodings found for any employees")
#             return jsonify(
#                 {
#                     "employee_name": "Unknown",
#                     "employee_id": None,
#                     "image_url": image_url,
#                 }
#             )

#         # Compare faces
#         matches = face_recognition.compare_faces(
#             known_face_encodings, face_encodings[0]
#         )
#         name = "Unknown"
#         employee_id = None

#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_face_names[first_match_index]
#             employee_id = known_employee_ids[first_match_index]
#             logging.debug(f"Match found: {name}, ID: {employee_id}")

#         return jsonify(
#             {"employee_name": name, "employee_id": employee_id, "image_url": image_url}
#         )
#     except Exception as e:
#         logging.error(f"Error in face recognition: {str(e)}")
#         return jsonify({"error": f"Face recognition failed: {str(e)}"}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import os
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient
import logging
from dotenv import load_dotenv
from bson.objectid import ObjectId

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Increase max content length
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# Validate Cloudinary configuration
cloudinary_name = os.getenv("CLOUDINARY_NAME")
cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")

if not all([cloudinary_name, cloudinary_api_key, cloudinary_api_secret]):
    logging.error("Missing Cloudinary credentials. Please check .env file.")
    raise ValueError("Missing Cloudinary credentials. Please check .env file.")

cloudinary.config(
    cloud_name=cloudinary_name,
    api_key=cloudinary_api_key,
    api_secret=cloudinary_api_secret,
)

# Validate MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
if not mongodb_uri:
    logging.error("Missing MONGODB_URI. Please check .env file.")
    raise ValueError("Missing MONGODB_URI. Please check .env file.")

try:
    client = MongoClient(mongodb_uri)
    db = client.FaceGate
    employees = db.employees
    client.server_info()
    logging.info("MongoDB connection successful.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise


@app.route("/recognize", methods=["POST"])
def recognize_face():
    logging.debug("Received request to /recognize")
    if "image" not in request.files:
        logging.error("No image provided in request")
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]
    employee_id = request.form.get("employeeId")
    logging.debug(f"Received image: {image_file.filename}, employeeId: {employee_id}")

    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(image_file)
        image_url = result["secure_url"]
        public_id = result["public_id"]  # Get public_id for deletion
        logging.debug(f"Uploaded to Cloudinary: {image_url}")

        # Reset file pointer after Cloudinary upload
        image_file.seek(0)

        # Load image for face recognition
        image = face_recognition.load_image_file(image_file)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            logging.error("No faces detected in image")
            cloudinary.uploader.destroy(public_id)  # Delete uploaded image
            return jsonify({"error": "No faces detected"}), 400

        # Fetch employee by ID if provided, otherwise return Unknown
        if not employee_id:
            logging.warning("No employeeId provided")
            cloudinary.uploader.destroy(public_id)
            return jsonify(
                {
                    "employee_name": "Unknown",
                    "employee_id": None,
                    "image_url": image_url,
                }
            )

        employee = employees.find_one(
            {"_id": ObjectId(employee_id)}, {"image": 1, "name": 1}
        )
        if not employee or "image" not in employee:
            logging.warning(f"No employee found with ID: {employee_id}")
            cloudinary.uploader.destroy(public_id)
            return jsonify(
                {
                    "employee_name": "Unknown",
                    "employee_id": None,
                    "image_url": image_url,
                }
            )

        # Load employee's image from Cloudinary URL
        import requests
        from io import BytesIO

        # from bson.objectid import ObjectId

        response = requests.get(employee["image"])
        response.raise_for_status()
        emp_image = face_recognition.load_image_file(BytesIO(response.content))
        emp_encoding = face_recognition.face_encodings(emp_image)

        if not emp_encoding:
            logging.warning(
                f"No face encoding found for employee {employee.get('name', 'unknown')}"
            )
            cloudinary.uploader.destroy(public_id)
            return jsonify(
                {
                    "employee_name": "Unknown",
                    "employee_id": None,
                    "image_url": image_url,
                }
            )

        # Compare faces
        match = face_recognition.compare_faces([emp_encoding[0]], face_encodings[0])[0]
        name = employee["name"] if match else "Unknown"
        emp_id = str(employee["_id"]) if match else None

        # Delete the uploaded image from Cloudinary
        cloudinary.uploader.destroy(public_id)
        logging.debug(f"Deleted image from Cloudinary: {public_id}")

        logging.debug(f"Recognition result: {name}, ID: {emp_id}")
        return jsonify(
            {
                "employee_name": name,
                "employee_id": emp_id,
                "image_url": image_url,
            }
        )
    except Exception as e:
        logging.error(f"Error in face recognition: {str(e)}")
        cloudinary.uploader.destroy(public_id)  # Ensure deletion on error
        return jsonify({"error": f"Face recognition failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
