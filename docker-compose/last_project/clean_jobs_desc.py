import json
from bs4 import BeautifulSoup as bs
from req import getData


def cJobs():

    jobs = getData() # [{},{}] //for now [{}]

    # title = ['ESSENTIAL FUNCTIONS AND RESPONSIBILITIES', 'EXPERIENCE']
    title = []
    val = [[],[],[]]
    dic = {}

    for dic_elem in list(range(len(jobs))):
        str_value = jobs[dic_elem]['jobDescription']
        soup = bs(str_value, 'lxml')
        for i in [0,1,2]:
            t = soup.select_one(f'h2:nth-of-type({i+1})')
            # print(t.find_next('ul'))
            title.append(t.string.strip()) # there is not homogeneous in jobDescription titles - <h2>
            for j in t.find_next('ul'):
                val[i].append(j.get_text(strip=True, separator='|').split('|')[0]) # output: ['', 'Collaborate closely with Product teams to understand and communicate the value of our offerings to both internal and external audiences', '', 'Orchestrate cross-functional product and market launches that deliver measurable outcomes', '', 'Help sales and marketing teams target and acquire revenue efficiently through effective positioning, marketing programs, marketing sizing, and business case analysis', '',....
                val[i] = list(filter(None, val[i])) #remove '' elements
            sub_title_num = list(range(len(val[i])))
            for k in sub_title_num:
                dic.update({f'{title[i]}_{k}': val[i][k]})

        jobs[dic_elem].pop('jobDescription')
        jobs[dic_elem].update(dic)

    js_jobs = json.dumps(jobs[0])
    # jobs[0] = jobs[0].replace("\'","\"") # json only allows enclosing strings with double quotes -- this {'id': 106116, 'jobTitle': 'Senior Product Marketing Manager', 'companyName': 'UpKeep', 'jobType': 'full-time', 'jobGeo': 'USA', 'jobLevel': 'Senior', 'pubDate': '2024-05-06 23:09:37', 'annualSalaryMin': '125000', 'annualSalaryMax': '130000', ... is not json
    # print(jobs[0])
    # print('---------------------------')
    # print(js_jobs)
    return js_jobs

# cJobs()