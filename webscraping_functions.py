"""
Functions for web-scraping tennis data

"""

__date__ = "2023-06-07"
__author__ = "SamKemp"


# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# %% --------------------------------------------------------------------------
# Get soup object
# -----------------------------------------------------------------------------
# Create an function for getting soup object
def get_soup_object(url):

    # Define url and user-agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

    # Set the user agent string in the headers
    headers = {
        'User-Agent': user_agent
    }

    # Make the request using the headers
    response = requests.get(url, headers=headers)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

# %% --------------------------------------------------------------------------
# Safe extract
# -----------------------------------------------------------------------------
def safe_extract(fn):
    try:
        return fn()
    except:
        return np.nan

# %% --------------------------------------------------------------------------
# Get tournament attributes
# -----------------------------------------------------------------------------
def get_tournament_name(url):

    # Get soup object 
    soup = get_soup_object(url)

    # Get attributes
    tournament_name = safe_extract(lambda: soup.title.text.split('-')[0].strip())

    return tournament_name


# %% --------------------------------------------------------------------------
# Get player attributes
# -----------------------------------------------------------------------------
def get_player_atts(url):

    # Get soup object 
    soup = get_soup_object(url)

    if 'Access Denied' in soup.text:
        print('Access Denied for tournament', url)
        time.sleep(600)  # Wait for 10 minutes
        soup = get_soup_object(url)
        
    name = safe_extract(lambda: soup.find('h1').text)
    rank = safe_extract(lambda: soup.find_all('h1')[1].text)
    points = safe_extract(lambda: soup.find_all('strong')[1].text)
    
    player_dict = {
    'name': name,
    'rank': rank,
    'points': points,
    }

    player_df = pd.DataFrame(player_dict, index=[0])

    return player_df

# %% --------------------------------------------------------------------------
# # Get player hyperlinks
# -----------------------------------------------------------------------------
# Create a function for adding player hyperlinks to a list
def get_player_links(url):

    players_url = url + '/teams'

    # Get soup object
    soup = get_soup_object(players_url)

    # Create an empty
    player_list = []

    # Loop through links and add player link if not already added
    for player in soup.find_all('a', class_='list-group-item'):
        player_link = 'https://s5.sir.sportradar.com' + player['href']
        if player_link not in player_list:
            player_list.append(player_link)

    return player_list

# %% --------------------------------------------------------------------------
# Get tournament player attributes
# -----------------------------------------------------------------------------
def get_tournament_player_df(tournament_url):

    # Get player hyperlinks
    tournament_players = get_player_links(tournament_url)

    #Create an empty list
    player_att_list = []

    # Loop through players and get attributes
    for player in tournament_players:
        new_row = get_player_atts(player)
        player_att_list.append(new_row)

    column_names = player_att_list[0].columns
    player_atts = np.array(player_att_list)
    player_atts = player_atts.reshape((player_atts.shape[0], player_atts.shape[-1]))
    player_atts = pd.DataFrame(player_atts, columns=column_names)

    return player_atts

# %% --------------------------------------------------------------------------
# Extract match result data
# -----------------------------------------------------------------------------
def get_match_df(tournament_url):

    # Set up Selenium to use a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Get tournament attributes
    tournament_name = get_tournament_name(tournament_url)

    # Load the web page with the table

    fixtures_url = tournament_url + '/fixtures/full'
    driver.get(fixtures_url)

    # Wait for the table to load by checking for a specific element on the page
    # that appears only after the table has been generated by JavaScript
    driver.implicitly_wait(10) 
    element = driver.find_elements('css selector', "#table-loaded")

    # Click the "show more" button if it's present
    try:
        show_more_button = driver.find_elements('xpath', '//*[@id="sr-container"]/div/div/div[4]/div/div/div/div/div[2]/div/div/div[2]/button')
        show_more_button[0].click()
        time.sleep(5) # wait for the new data to load
    except:
        pass

    driver.implicitly_wait(10) # wait for up to 10 seconds
    element = driver.find_elements('css selector', "#table-loaded")

    # Extract the HTML code of the entire page, including the dynamically generated table
    html = driver.page_source

    # Parse the HTML code using Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Find the table using Beautiful Soup's find() or find_all() method
    table = soup.find("table")

    # Extract the data from the table as needed
    rows = table.find_all("tr")

    # Get match info
    match_dicts = []

    for row in rows:
        if '/' in row.text:
            date = row.find('td').text
            continue
        try:
            players = row.find_all('td')[1].text.split('-')
            both_players = [player[:-3] for player in players]
            home_player = both_players[0]
            away_player = both_players[1]

            scores_set = row.find_all('td')[-1].text.split(':')
            scores_set = ':'.join([score[0] for score in scores_set][:2]) 

            match_dict = {
                'tournament_name': tournament_name,
                'date': date,
                'player1': home_player,
                'player2': away_player,
                'match_result': scores_set
            }

            match_dicts.append(match_dict)
                
        except:
            continue

    # Close the headless browser
    driver.quit()

    # Create a dataframe
    match_df = pd.DataFrame(match_dicts)

    return match_df

# %% --------------------------------------------------------------------------
# Merge player atts and matches
# -----------------------------------------------------------------------------
def merge_player_atts_matches(matches_df, player_atts_df):

    # Create copies for home and away players
    home_atts = player_atts_df.copy()
    away_atts = player_atts_df.copy()

    # Rename columns
    home_atts = home_atts.rename({'name':'player1', 'rank':'rank_home','points':'pts_home'}, axis=1)
    away_atts = away_atts.rename({'name':'player2', 'rank':'rank_away','points':'pts_away'}, axis=1)
    
    # Merge with match_df
    matches_df2 = pd.merge(matches_df, home_atts, on='player1')
    matches_df3 = pd.merge(matches_df2, away_atts, on='player2')

    return matches_df3