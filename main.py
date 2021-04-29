import requests as req

# get all episodes
rEps = req.get('https://www.breakingbadapi.com/api/episodes')

# check status code
if rEps.status_code == 200:
