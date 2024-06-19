import requests
import pandas as pd
from saveS3 import SaveS3
from bs4 import BeautifulSoup

def GetAPIData(tag, count):
    ENDPOINT = f'https://jobicy.com/api/v2/remote-jobs?count={count}&tag={tag}'
    req = requests.get(ENDPOINT)
    if req.status_code == 200:
        data = req.json()
        jobs = data['jobs']
        return jobs
    else:
        return []

def jobs_data(jobs):
    jobs_items = jobs
    for i in range(len(jobs_items)):
        # Ensure jobType is a string, not a list
        if isinstance(jobs_items[i]['jobType'], list):
            jobs_items[i]['jobType'] = jobs_items[i]['jobType'][0]

        # Remove unwanted keys
        keys_rem = ['url', 'jobSlug', 'companyLogo', 'jobIndustry', 'jobExcerpt']
        for key in keys_rem:
            jobs_items[i].pop(key, None)

        # Ensure all necessary fields are present
        jobs_items[i] = {
            'id': jobs_items[i].get('id', ""),
            'jobTitle': jobs_items[i].get('jobTitle', ""),
            'companyName': jobs_items[i].get('companyName', ""),
            'jobType': jobs_items[i].get('jobType', ""),
            'jobGeo': jobs_items[i].get('jobGeo', ""),
            'jobLevel': jobs_items[i].get('jobLevel', ""),
            'pubDate': jobs_items[i].get('pubDate', ""),
            'AnnualSalaryMin': jobs_items[i].get('annualSalaryMin', ""),
            'AnnualSalaryMax': jobs_items[i].get('annualSalaryMax', ""),
            'SalaryCurrency': jobs_items[i].get('salaryCurrency', "")
        }
    return jobs_items

def jobs_descriptions(jobs):
    description_data = []

    for job in jobs:
        job_id = job['id']
        if 'jobDescription' in job:
            soup = BeautifulSoup(job['jobDescription'], 'html.parser')
            description_elements = soup.find_all(['p', 'li', 'h2'])

            current_header = None

            # Reiniciar el índice para cada nuevo id de trabajo
            idx = 1

            # Contador de elementos
            element_count = 0

            for element in description_elements:
                if element.name == 'h2':
                    current_header = element.get_text().strip()
                else:
                    if element_count < 20:
                        description_data.append({
                            'idx': idx,
                            'id': job_id,
                            'descriptionType': current_header,
                            'description': element.get_text().strip()
                        })
                        idx += 1
                        element_count += 1
                    else:
                        break  # Salir del bucle si ya se han agregado n elementos
    return description_data

if __name__ == "__main__":
    # Define parameters
    tag = 'Business+Intelligence'
    count = 2
    args = GetAPIData(tag, count)

    # Process jobs descriptions
    jobs_desc = jobs_descriptions(args)
    jobs_desc_df = pd.DataFrame(jobs_desc)
    print(jobs_desc_df)
    jobs_desc_df.info()

    # Process main job data
    jobs_main = jobs_data(args)
    jobs_main_df = pd.DataFrame(jobs_main)
    print(jobs_main_df)
    jobs_main_df.info()

    # Upload dataframes to MinIO
    up1 = SaveS3(jobs_desc_df, 'jobsbucket', 'jobs_descriptions')
    s3_obj1 = up1.write_to_minio_parquet()
    print(s3_obj1)

    up2 = SaveS3(jobs_main_df, 'jobsbucket', 'jobs_main')
    s3_obj2 = up2.write_to_minio_parquet()
    print(s3_obj2)
