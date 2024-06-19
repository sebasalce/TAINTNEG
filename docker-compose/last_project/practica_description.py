import requests
from bs4 import BeautifulSoup
import pandas as pd


def parseJobDescriptions(tag, count):
    ENDPOINT = f'https://jobicy.com/api/v2/remote-jobs?count={count}&tag={tag}'


    req = requests.get(ENDPOINT)
    if req.status_code == 200:
        data = req.json()
        jobs = data['jobs']
        
        description_data = []

        for job in jobs:
            job_id = job['id']
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

        return pd.DataFrame(description_data)
    else:
        return pd.DataFrame()

# Define parameters
tag = 'Business+Intelligence'
count = 2

# Fetch data
descriptions_data = parseJobDescriptions(tag, count)

# Save data to CSV file
descriptions_data.to_csv('descriptions_data.csv', index=False)

print(descriptions_data)
