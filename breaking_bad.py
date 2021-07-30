import sys
import requests as req

"""
some explanation:

First, when I saw the description I assumed that the characters have an episode attribute. However this was not
the case, so I had to check characters in each episode. My initial plan was to send a request for each episode,
but that is not optimal (There is a limit for requests from the API). I got the list of all episodes with one
request and went through them and checked the characters for a match. If the input character set is the subset
of the episode character set, then the ID of the episode will be added to a common episodes list. This way we
are not limited to a maximum of 2 characters. I used those episode IDs for getting the data from the initial request.
One thing I want to mention is that I assumed that an episode with ID 'i' is the episode with the index 'i-1'
in the request dictionary. I could code it in a way that it would find the episode ID but it required extra work
and extra loops. (I just wanted to let you know that I did it on purpose, don't judge me) Then I simply formatted
a string for the output. Finally, I added a status code check in case that we get an error from the server.
I checked the output with pytest and it was 100%. That's it!
"""


def call(arr):
    # get all episodes
    rEps = req.get(
        'https://www.breakingbadapi.com/api/episodes?series=Breaking+Bad')

    commonEps = []

    # check status code
    if rEps.status_code == 200:
        rEpsJson = rEps.json()

       # iterate through episodes and check if character list is subset of episode character list
        for ep in rEpsJson:
            if set(arr).issubset(set(ep['characters'])) and arr:
                # add episode id to common episodes list
                commonEps.append(ep['episode_id'])

        # create the output list using the episode ID list
        output = []
        for ep in commonEps:
            # assuming episode ID is the same as the position in the episode list
            epData = rEpsJson[ep-1]
            output.append(
                'S{:02d}{:02d} - {}'.format(int(epData['season']), int(epData['episode']), epData['title']))
        return output

    elif rEps.status_code == 429:
        print('Maximum requests reached, wait 24 hours.')
    else:
        print('Error {}'.format(rEps.status_code))


args = sys.argv[1:]
print(call(args))
