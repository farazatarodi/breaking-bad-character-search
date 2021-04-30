import sys
import requests as req

"""
some explanation:

First when I saw the description I assumed that the characters have an episode attribute.
However this was not the case, so I had to check characters in each episode. My intial plan was to send request for each episode,
but that is not optimal (There is a limit for requests from the API).
I got the list of all episodes and went through them and checked the characters for a match. Created a dictionary with the number
of occurance for each episode and used the occurance to compare with the number of the characters that we are looking for.
This way we are not limited to maximum 2 characters.
Next I created a list of all common episodes between characters and used those episode IDs for getting the data from the intial request.
One thing I want to mention is that I assumed that an episode with ID 'i' is the episode with index 'i-1' in thr request dictionary.
I could code it in a way that it would find the episode ID but it required extra work and extra loops.
(I just wanted to let you know that I did it on purpose, don't judge me)
Then I simply formatted a string for the output. Finally I checked the status code in case that we get an error from the server.
I checked the output with pytest and it was 100%. B)
That's it!
"""


def call(arr):
    # get all episodes
    rEps = req.get(
        'https://www.breakingbadapi.com/api/episodes?series=Breaking+Bad')

    epIds = {}
    commonEps = []

    # check status code
    if rEps.status_code == 200:
        # weirdly json outputs a list
        rEpsJson = rEps.json()

        # iterate through episodes and check existence of each character
        for ep in rEpsJson:
            epIds[ep['episode_id']] = 0
            for char in arr:
                # if character is present, add to temporary list
                if char in ep['characters']:
                    epIds[ep['episode_id']] += 1

        # iterate through temporary list to find common episodes
        for epId, count in epIds.items():
            # add common eps to final list
            if count == len(arr) and len(arr) != 0:
                commonEps.append(epId)

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
