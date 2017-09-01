import pandas as pd
import itertools
import praw
import json
from pprint import pprint

dichotomies = [('E', 'I'), ('N', 'S'), ('T', 'F'), ('P', 'J')]
personality_types_tuples = list(itertools.product(*dichotomies))
personality_types = [''.join(pt_tuple) for pt_tuple in personality_types_tuples]

pt_dist_url = 'https://www.careerplanner.com/MB2/TypeInPopulation.cfm'
pt_dist_df = pd.read_html(pt_dist_url)
pt_dist_df = pt_dist_df[-1]

pt_dist_df[2][0] = pt_dist_df[1][0]
del pt_dist_df[1]

pt_dist_df.columns = pt_dist_df.iloc[0]
pt_dist_df = pt_dist_df[1:]
# Convert string percentage to numeric
pt_dist_df['Frequency in Population'] = pd.to_numeric(pt_dist_df['Frequency in Population'].str.strip('%'))/100
print(pt_dist_df)

with open('authentication.json') as file:
    auth = json.load(file)

reddit = praw.Reddit(client_id=auth['client_id'], client_secret=auth['client_secret'],
                     password=auth['password'], user_agent=auth['user_agent'],
                     username=auth['username'])

pt_sr_info_df = pd.DataFrame()
pt_sr_info_df.columns = ['display_name', 'created_utc', 'description', 'name', 'subscribers']
pt_sr_names = []
for ptype in personality_types:
    sr_name = reddit.subreddit(ptype).name
    pt_sr_names.append(sr_name)

for sr_info in reddit.info(pt_sr_names):
    sr_info_vars = vars(sr_info)
    pt_sr_info_df[sr_info_vars['display_name']] = sr_info_vars