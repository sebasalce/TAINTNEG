import requests

role = 'business intelligence'
num_jobs = 1
# jobs = {}

ENDPOINT_API = f'https://jobicy.com/api/v2/remote-jobs?count={num_jobs}&tag={role}'

def getData():
    req = requests.get(ENDPOINT_API)
    if req.status_code == 200:
        dat = req.json()
        
    for i in list(range(num_jobs)):
        jobs = dat['jobs'] # list [{},{}]
        # print(f'raw data: {jobs}')
        if type(jobs[i]['jobType']) == list:
            jobs[i]['jobType'] = jobs[i]['jobType'][0]
        keys_rem = ['url', 'jobSlug', 'companyLogo', 'jobIndustry', 'jobExcerpt', ]
        for key in keys_rem:
            if key in jobs[i]:
                jobs[i].pop(key)
    
    return jobs
    # print(jobs)


# getData()