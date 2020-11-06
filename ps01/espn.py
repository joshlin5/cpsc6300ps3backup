import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

NCAAF_URL="https://www.espn.com/college-football/teams"

def fetch_ncaaf_teams(url=NCAAF_URL):
    """Fetch the list of ncaa football teams
    
    Args:
        url (string): the url of the web page for ncaa football teams 
    
    Returns:
            
    """
    teams = []
    
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    
    conferences = soup.find_all("div", class_="headline")
    for conference in conferences:
        conference_name = conference.get_text()
        team_links = conference.parent.find_all("a", class_="AnchorLink")
        for team_link in team_links:
            if team_link.find("h2"):
                team_url = team_link['href']
                team_name = team_link.get_text()
                team_id = int(team_url.split("/")[-2])
                teams.append({"id": team_id, "name": team_name, "conference": conference_name, "url": team_url})
    return teams
