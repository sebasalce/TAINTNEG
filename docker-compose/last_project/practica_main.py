import requests
import json

role = 'business intelligence'
num_jobs = 1

ENDPOINT_API = f'https://jobicy.com/api/v2/remote-jobs?count={num_jobs}&tag={role}'

def getData():
    req = requests.get(ENDPOINT_API)
    if req.status_code == 200:
        dat = req.json()
        jobs = dat['jobs']  # list of job dictionaries
        
        for i in range(len(jobs)):
            # Ensure jobType is a string, not a list
            if isinstance(jobs[i]['jobType'], list):
                jobs[i]['jobType'] = jobs[i]['jobType'][0]

            # Remove unwanted keys
            keys_rem = ['url', 'jobSlug', 'companyLogo', 'jobIndustry', 'jobExcerpt']
            for key in keys_rem:
                jobs[i].pop(key, None)

            # Ensure all necessary fields are present
            jobs[i] = {
                'id': jobs[i].get('id', ""),
                'jobTitle': jobs[i].get('jobTitle', ""),
                'companyName': jobs[i].get('companyName', ""),
                'jobType': jobs[i].get('jobType', ""),
                'jobGeo': jobs[i].get('jobGeo', ""),
                'jobLevel': jobs[i].get('jobLevel', ""),
                'pubDate': jobs[i].get('pubDate', ""),
                'AnnualSalaryMin': jobs[i].get('annualSalaryMin', ""),
                'AnnualSalaryMax': jobs[i].get('annualSalaryMax', ""),
                'SalaryCurrency': jobs[i].get('salaryCurrency', "")
            }
    
        return jobs

# Fetch and process data
jobs_data = getData()

# Convert jobs data to JSON format
jobs_json = json.dumps(jobs_data)

# Print jobs data in JSON format
print(jobs_json)

# Optionally, save the JSON to a file
with open('jobs_data.json', 'w') as f:
    f.write(jobs_json)
