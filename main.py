import requests
import pandas as pd
import itertools

dichotomies = [('E', 'I'), ('N', 'S'), ('T', 'F') ,('P', 'J')]
personality_types_tuples = list(itertools.product(*dichotomies))
personality_types = [''.join(pt_tuple) for pt_tuple in personality_types_tuples]

pt_dist_url = 'https://www.careerplanner.com/MB2/TypeInPopulation.cfm'

pt_dist_req = requests.get(pt_dist_url).content
pt_dist_df = pd.read_html(pt_dist_req)
df = pt_dist_df[-1]
print(df)