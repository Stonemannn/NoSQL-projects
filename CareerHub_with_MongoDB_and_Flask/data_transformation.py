import pandas as pd
import json

# Function to merge all dataframes based on 'id'
def merge_dataframes(dfs, key):
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=key, how='left')
    return merged_df

# Read the CSV files into DataFrames
companies_df = pd.read_csv('mp2-data/companies.csv')
education_and_skills_df = pd.read_csv('mp2-data/education_and_skills.csv')
employment_details_df = pd.read_csv('mp2-data/employment_details.csv')
industry_info_df = pd.read_csv('mp2-data/industry_info.csv')
jobs_df = pd.read_csv('mp2-data/jobs.csv')

# Merge all dataframes based on 'id'
all_data = merge_dataframes([jobs_df, companies_df, education_and_skills_df, employment_details_df, industry_info_df], 'id')

# Convert the merged DataFrame into a list of dictionaries
records = all_data.to_dict(orient='records')

# Transform the data into nested JSON structure
transformed_records = []
for record in records:
    transformed_record = {
        'job_id': record['id'],
        'title': record['title'],
        'industry': record['industry_name'],
        'average_salary': record['average_salary'],
        'description': record['description_x'],
        'detailed_description': record['detailed_description'],
        'years_of_experience': record['years_of_experience'],
        'responsibilities': record['responsibilities'],
        'requirements': record['requirements'],
        'company': {
            'name': record['name'],
            'size': record['size'],
            'type': record['type'],
            'location': record['location'],
            'website': record['website'],
            'description': record['description_y'],
            'hr_contact': record['hr_contact']
        },
        'employment_details': {
            'employment_type': record['employment_type'],
            'benefits': record['benefits'],
            'remote': record['remote']
        },
        'education_and_skills': {
            'required_education': record['required_education'],
            'preferred_skills': record['preferred_skills']
        },

    }
    transformed_records.append(transformed_record)

# Save the transformed data as a JSON file
with open('transformed_data.json', 'w') as f:
    json.dump(transformed_records, f, indent=4)
