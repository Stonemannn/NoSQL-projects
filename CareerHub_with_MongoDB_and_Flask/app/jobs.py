'''Module for serving API requests'''

from app import app
from bson.json_util import dumps, loads
from flask import request, jsonify
import json
import ast # helper library for parsing data from string
from importlib.machinery import SourceFileLoader
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient(host="localhost", port=27017)

# Import the utils module
#  '*' is used, which means the name is not specifically set
utils = SourceFileLoader('*', './app/utils.py').load_module()

# Select the database
db = client.careerhub
# Select the collection
collection = db.jobs


# route decorator that defines which routes should be navigated to this function
@app.route("/") # '/' for directing all default traffic to this function get_initial_response()
def get_initial_response():

    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to my CareerHub API'
    }
    # jsonify is a Flask utility function that is commonly used for handling HTTP responses.
    # It not only serializes the Python object to JSON 
    # but also wraps it in a Flask Response object with the application/json mimetype, 
    # which is an HTTP header that tells the client the type of content being sent.
    resp = jsonify(message)
    # Returning the object
    return resp




@app.route("/create/jobPost", methods=['POST'])
def create_jobs():
    '''
       Function to create new job(s)
    '''
    try:
        # Create new users

        try:
            body = request.get_json()
            print("Received body:", body)  # Debug line
        except Exception as e:
            print("Error in receiving body:", e)  # Debug line
            return "Bad request", 400

        # Check whether job id, job title and industry are provided
        for record in body:
            if not record.get('job_id') or not record.get('title') or not record.get('industry'):
                return "Please provide job_id, title and industry", 400
            
            # Check if job_id already exists in the database
            existing_record = collection.find_one({"job_id": record.get('job_id')})
            if existing_record:
                return f"A job with job_id {record.get('job_id')} already exists", 400


        record_created = collection.insert_many(body)

        # Check if the records are created
        if record_created:
            inserted_id = record_created.inserted_ids
            # Prepare the response
            # If inserted_id is a list, then many records were inserted
            if isinstance(inserted_id, list):
                # Return list of Id of the newly created item

                # Convert ObjectId to string for JSON serialization
                # ObjectId is a BSON type 
                # that Python's standard jsonify function doesn't know how to serialize into JSON.
                ids = []
                for _id in inserted_id:
                    ids.append(str(_id))

                return jsonify(ids), 201
            else:
                # Return Id of the newly created item
                return jsonify(str(inserted_id)), 201
            
    except Exception as e:
        # Error while trying to create customers
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500




@app.route('/search_by_job_id/<job_id>', methods=['GET'])
def get_by_id(job_id):
    try:
        # Query the document
        result = collection.find_one({"job_id": int(job_id)})
        
        # If document not found
        if not result:
            return jsonify({"message": "Job not found"}), 404
        
        # Convert ObjectId to string
        result['_id'] = str(result['_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# Update by job title
# Note: arguments are string type by default, so convert your args as needed
@app.route("/update_by_job_title/<title>", methods=['POST'])
def update_job_title(title):
    '''
       Function to update the job by title. 
       But in case of multiple jobs with the same title, user can select which job to update by adding job_id
    '''
    try:
        # Get the value which needs to be updated
        try:
            body = request.get_json()
            print(body)
        except Exception as e:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return 'Bad request', 400

        # Find all records with the given title
        records = collection.find({"title": title})
        records_count = collection.count_documents({"title": title})

        # If multiple records are found with the same title
        if records_count > 1:
            job_list = []
            for record in records:
                job_list.append({
                    "job_id": record.get("job_id"),
                    "title": record.get("title"),
                    "description": record.get("description"),
                    "industry": record.get("industry")
                })

            # Ask user to select which job to update
            return jsonify({"message": "Multiple jobs found with the same title. Please select one to update.", "jobs": job_list}), 300

        # If only one record is found, proceed to update
        elif records_count == 1:
            records_updated = collection.update_one({'title': title}, {'$set': body[0]})

            return jsonify(records_updated.raw_result), 200

        else:
            return "No jobs found with the given title", 404

    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500
    

# In case there are multiple jobs with the same title, user can select which job to update by job_id
@app.route("/update_by_job_title/<title>/<job_id>", methods=['POST'])
def update_job_by_title_id(title,job_id):
    '''
       Function to update the job by both title and job_id.
    '''
    try:
        try:
            body = request.get_json()
            print(body)
        except Exception as e:
            return 'Bad request', 400

        records_updated = collection.update_one({'title': title, "job_id": int(job_id)}, {'$set': body[0]})
        return jsonify(records_updated.raw_result), 200

    except Exception as e:
        print(e)
        return 'Server error', 500




@app.route("/delete_by_job_title/<title>", methods=['DELETE'])
def remove_job(title):
    """
       Function to remove the jobs.
    """
    confirm = request.args.get('confirm', type=bool, default=False)

    if not confirm:
        return 'Confirmation required', 400

    try:
        delete_job = collection.delete_many({"title": title})

        print(delete_job.raw_result)
        if delete_job.deleted_count > 0 :
            # Prepare the response
            return 'Job(s) removed', 200
        else:
            # Resource not found
            return 'Job not found', 404
    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "Server error", 500




# Salary Range Query
@app.route("/search_by_salary", methods=['GET'])
def fetch_jobs_by_salary():
    min_salary = request.args.get('min_salary')
    max_salary = request.args.get('max_salary')

    if not min_salary or not max_salary:
        return jsonify({"error": "Both min and max_salary parameters are required"}), 400

    jobs_found = collection.find({
            "average_salary": {
                # NOTE!!!! the data type of the salary is string, we need to convert it to int
                "$gte": int(min_salary),
                "$lte": int(max_salary)
            }})

    # Convert ObjectId to string for each document
    results = []
    for job in jobs_found:
            job["_id"] = str(job["_id"])
            results.append(job)

    return jsonify(list(results)), 200
    

@app.route("/search_by_experience_level", methods=['GET'])
def fetch_jobs_by_experience_level():
    experience_level = request.args.get('experience_level')

    if not experience_level:
        return jsonify({"error": "Experience level is required"}), 400

    if experience_level == "entry_level":

        jobs_found = collection.find({
            "years_of_experience": {
                "$lte": 3
            }})
        
    elif experience_level == "mid_level":

        jobs_found = collection.find({
            "years_of_experience": {
                "$gt": 3,
                "$lte": 6
            }})
    
    elif experience_level == "senior_level":

        jobs_found = collection.find({
            "years_of_experience": {
                "$gt": 6
            }})

    # Convert ObjectId to string for each document
    results = []
    for job in jobs_found:
            job["_id"] = str(job["_id"])
            results.append(job)

    return jsonify(list(results)), 200
        





@app.errorhandler(404)
def page_not_found(e):
    '''Send message to the user if route is not defined.'''

    message = {
        "err":
            {
                "msg": "This route is currently not supported."
            }
    }

    resp = jsonify(message)
    # Sending 404 (not found) response
    resp.status_code = 404
    # Returning the object
    return resp