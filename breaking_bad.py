import sys
import requests as req


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
