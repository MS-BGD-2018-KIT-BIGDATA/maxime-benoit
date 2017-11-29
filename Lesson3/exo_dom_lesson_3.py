import requests
from bs4 import BeautifulSoup
import json
import math
import operator

######## get list of contributors ########

url = "https://gist.github.com/paulmillr/2657075"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')

tab = soup.find_all("tbody")[0]
lines = tab.find_all("tr")

contributors = []
for line in lines:
    contributors.append(line.find_all('a', href=True)[0].text)

######## get avg of stars for a contributor ########

def get_avg_of_stars(contributor):

    page = 1
    nb_of_stars = 0
    nb_of_repo = 0

    # get all repositorie stars

    while(True):

        api = 'https://api.github.com/users/' + contributor + \
            '/repos?access_token=fb59a164adda3d6521352f952561dc4e2d10e8d5&page=' + \
            str(page)

        json_content = requests.get(api).text

        repos = json.loads(json_content)

        if repos == []:
            break

        for repo in repos:
            nb_of_stars += int(repo['stargazers_count'])

        nb_of_repo += len(repos)

        page += 1

    if nb_of_repo == 0:
        return 0

    return nb_of_stars/nb_of_repo

######## save results ########

contributors_avg_of_stars = {}

i = 1
for contributor in contributors:
    contributors_avg_of_stars[contributor] = get_avg_of_stars(contributor)
    print("\ncontributor " + contributor + ": OK") # track contributor
    print("\n " + str(i) + "/" + str(len(contributors))) # track progression
    i += 1


######## sort results ########

sorted_contributors_avg_of_stars = sorted(
    contributors_avg_of_stars.items(), key=operator.itemgetter(1), reverse=True)

######## print results ########

print('')
for i in range(len(sorted_contributors_avg_of_stars)):

    print(str(i+1) + '. ' + sorted_contributors_avg_of_stars[i][
          0] + ' : ' + str(math.floor(sorted_contributors_avg_of_stars[i][1]*100)/100) + ' stars')
