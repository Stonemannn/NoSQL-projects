# README for CareerHub API

## Overview
This is a Flask API for a job portal called CareerHub. It uses MongoDB as a database to manage job-related data.

## Setup: Data Transformation
### Data Transformation Script

This Python script merges job-related data from multiple CSV files and saves it as a nested JSON file. 

### How to Run
1. Place all CSV files in `mp2-data/`.
2. Run the script.
3. Output is saved as `transformed_data.json`.




## Endpoints
# README for CareerHub API

## Overview
This is a Flask API for a job portal called CareerHub, which interacts with a MongoDB database to manage job postings and related data.

## Requirements
- Python 3.x
- Flask
- PyMongo

## Setup
1. Make sure MongoDB is running on `localhost`, port `27017`.
2. Place the `utils.py` file in the `./app/` directory.

## Endpoints and Examples

### 1. GET `/`
- **Description**: Initial greeting for the API.
- **Example Response**: 
    ```json
    {
      "apiVersion": "v1.0",
      "status": "200",
      "message": "Welcome to my CareerHub API"
    }
    ```

### 2. POST `/create/jobPost`
- **Description**: Creates new job postings.
- **Request Body**: JSON array of job records.
- **Example Request Body**:
    ```json
    [
      {
        "job_id": 1,
        "title": "Software Engineer",
        "industry": "Technology"
      }
    ]
    ```
- **Example Response**:
    ```json
    ["5dacf3f4abcd123456efghijk"]
    ```

### 3. GET `/search_by_job_id/<job_id>`
- **Description**: Fetches job details by `job_id`.
- **Example URL**: `/search_by_job_id/1`
- **Example Response**:
    ```json
    {
      "job_id": 1,
      "title": "Software Engineer",
      "industry": "Technology",
      "_id": "5dacf3f4abcd123456efghijk"
    }
    ```

### 4. POST `/update_by_job_title/<title>`
- **Description**: Updates job details by `title`. If multiple jobs with the same title exist, the user is prompted to specify which job to update by `job_id`.
- **Example URL**: `/update_by_job_title/Software%20Engineer`
- **Example Request Body**:
    ```json
    [
      {
        "industry": "Tech"
      }
    ]
    ```
- **Example Response**: 
    ```json
    {
      "ok": 1,
      "nModified": 1,
      "n": 1
    }
    ```

### 5. POST `/update_by_job_title/<title>/<job_id>`
- **Description**: Updates job details by both `title` and `job_id`.
- **Example URL**: `/update_by_job_title/Software Engineer/1`
- **Example Request Body**:
    ```json
    [
      {
        "industry": "IT"
      }
    ]
    ```
- **Example Response**: 
    ```json
    {
      "ok": 1,
      "nModified": 1,
      "n": 1
    }
    ```

### 6. DELETE `/delete_by_job_title/<title>`
- **Description**: Deletes job(s) by `title`. Requires query parameter `confirm=true` for confirmation.
- **Example URL**: `/delete_by_job_title/Software Engineer?confirm=true`
- **Example Response**: `Job(s) removed`

### 7. GET `/search_by_salary`
- **Description**: Searches jobs by salary range. Requires `min_salary` and `max_salary` as query parameters.
- **Example URL**: `/search_by_salary?min_salary=50000&max_salary=100000`
- **Example Response**: 
    ```json
    [
      {
        "job_id": 1,
        "title": "Software Engineer",
        "average_salary": 75000,
        "_id": "5dacf3f4abcd123456efghijk"
      }
    ]
    ```

### 8. GET `/search_by_experience_level`
- **Description**: Searches jobs by experience level. Requires `experience_level` as a query parameter which can be either `entry_level`, `mid_level`, or `senior_level`.
- **Example URL**: `/search_by_experience_level?experience_level=entry_level`
- **Example Response**: 
    ```json
    [
      {
        "job_id": 1,
        "title": "Software Engineer",
        "years_of_experience": 2,
        "_id": "5dacf3f4abcd123456efghijk"
      }
    ]
    ```

## How to Run
1. Run `app.py`.

## Error Handling
- 400: Bad Request
- 404: Not Found
- 500: Server Error

## Author
Jiayu Shi


