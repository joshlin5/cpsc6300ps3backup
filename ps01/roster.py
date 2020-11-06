
# YOUR CODE HERE
#raise NotImplementedError()
import requests
import re
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

def get_team_url(team_id, team_name):
    url = "https://www.espn.com/college-football/team/roster/_/id/" + str(team_id) + "/"
    real_team_name = team_name.split( )
    #print(real_team_name)
    i = 1
    while (len(real_team_name) > i):     
        url = url + real_team_name[i-1].lower()+"-"
        i = i + 1
    else: 
        url = url + real_team_name[i-1].lower()
    return url

def extract_team_roster(team_id, team_name):
    """
    Extract the team roster for a NCAA college football team
    
    Args:
        team_id: the id of a NACC football team assigned by ESPN
        team_name: the name of the football team
        
    Returns:
        a list of dict representing the roster of the entire team.
    """
    #team_id = 150
    #team_name = "Duke Blue Devils"
    roster = []
    def mysplit(s, ex):
        head = s.rstrip(ex)
        tail = s[len(head):]
        return head, tail
    
    def is_player_row(tag):
        if tag.name == 'tr' and tag.has_attr('data-idx'):
            return True
        return False
    
    #Computing Team URL
    url = get_team_url(team_id, team_name)

    #Create a BeautifulSoup Object
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
        
    #Finding Team Name
    team_tag = soup.find('h1', string=re.compile(' Roster$'))
        
    #Searching For Team Group
    groups = soup.find_all(class_="Table__Title", string=["Offense", "Defense", "Special Teams"])
    #print(len(groups), "groups")
    #for g in groups:
        #print(g)
        
    #Finding the Column Names
    col_names = []
    for g in groups:
        t = g.find_next("table")
        for c in t.thead.tr.children:
            col_names.append(c.text)
        
    #Find the Attributes of a Player
    players = []
    id_list = []
    for x in groups :
        table = x.find_next("table")
        for c in table.tbody.find_all(is_player_row):
            tds = c.find_all('td')
            cols = []
            for td in tds:
                cols.append(td.get_text())
            players.append(cols)
        for aPlayer in players :
            player = {}
            name = mysplit(aPlayer[1], '0123456789')
            player["player_name"] = name[0]
            
            player_url_name = name[0].split()
            #print(player_url_name)
            totalURL = ""
            i = 1
            for x in player_url_name :
                #print(x)
                if i != len(player_url_name) :
                    if x.find(".") :
                        x = x.replace('.', '') 
                    if x.find('\'') :
                        #print(x)
                        x = x.replace('\'', '') 
                    if x.find(',') :
                        x = x.replace(',', '')
                    #print(x)
                    totalURL = totalURL + x.lower() + "-"
                else :
                    if x.find(".") :
                        x = x.replace('.', '')
                    if x.find('\'') :
                        #print(x)
                        x = x.replace('\'', '') 
                    if x.find(',') :
                        x = x.replace(',', '')
                    if x != '' :
                        #print(x)
                        totalURL = totalURL + x.lower()
                i = i + 1
            totalURL = '/' + totalURL
            #print(totalURL)
            #print(soup.find('a', href=re.compile(totalURL))['href'])
            id = soup.find('a', href=re.compile(totalURL))['href']
            id = re.sub('http://www.espn.com/college-football/player/_/id/', '', id)
            id = re.sub(totalURL, '', id)
            if id_list.count(id) == 0: 
                id_list.append(id)
                player["player_id"] = id
                if name[1] == '' :
                    player["player_no"] = "NA"
                else :
                    player["player_no"] = name[1]
                player["POS"] = aPlayer[2]
                player["HT"] = aPlayer[3]
                player["WT"] = aPlayer[4]
                player["Class"] = aPlayer[5]
                player["Birthplace"] = aPlayer[6]
                #print(player)
                roster.append(player)
        
    # YOUR CODE HERE
    #raise NotImplementedError()
    return roster
