# Import Dependencies
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import warnings
import requests
import shutil
from IPython.display import Image
warnings.filterwarnings('ignore')


def init_browser():
    # Path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_latest_details():
    # Initialize browser
    browser = init_browser()
    mars_data = {}

    # Visit Nasa news url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve article containing latest information
    article = soup.find("div", class_='list_text')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

    # Store scrapped data
    mars_data['news_title'] = news_title
    mars_data['news_article'] = news_p

    # return mars_data


# def scrape_featured_image():
#     # Path to the chromedriver
#     browser = init_browser()

    # Visit JPL Featured Space Image url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click on "FULL IMAGE" button
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    # Click on "more info" button
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # HTML Object
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve image url
    image_url = image_soup.find('img', class_='main_image')['src']

    # Obtain complete featured image url
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    # Store scrapped data
    mars_data['featured_image_url'] = featured_image_url

    # return mars_data


# def scrape_latest_tweet():
#     # Path to the chromedriver
#     browser = init_browser()

    # Path to the chromedriver
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)

    # HTML Object
    html_tweet = browser.html

    # Parse HTML with Beautiful Soup
    tweet_soup = BeautifulSoup(html_tweet, 'html.parser')
    time.sleep(5)

    # Find all tweets
    twitter = tweet_soup.find_all('span')
    time.sleep(5)

    # Select first tweet in all tweets
    for tweet in twitter:
        if tweet.text != '' and 'InSight' in tweet.text:
            break

        # Store scrapped data
        mars_data['latest_tweet'] = tweet.text

#     return mars_data
#
#
# def scrape_facts():

    # Path to the chromedriver
    url = 'https://space-facts.com/mars/'

    # Using Pandas to scrape the table on the website
    df = pd.read_html(url)
    profile = df[0]
    profile.rename(columns={0: "Report", 1: "Values"}, inplace=True)
    profile.set_index("Report", inplace=True)

    # Convert and save to html
    profile_html = profile.to_html()
    profile_html = profile_html.replace("\n", "")

    # Store scrapped data
    mars_data['Mars_Planet_Profile'] = profile_html


#     return mars_data
#
#
# def scrape_hemi_image_urls():
#     # Path to the chromedriver
#     browser = init_browser()

    # Path to the chromedriver
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)

    # HTML Object
    all_html = browser.html

    # Parse HTML with Beautiful Soup
    all_soup = BeautifulSoup(all_html, 'html.parser')
    time.sleep(5)

    # Find all hemisphere image links
    all_links = all_soup.find_all('div', class_='description')

    # Make an empty list to store the links
    hemi_image_urls = []

    for i in all_links:
        browser.visit('https://astrogeology.usgs.gov' + i.a['href'])
        time.sleep(5)
        browser.click_link_by_partial_text('Open')
        time.sleep(5)

        # HTML Object
        full_image = browser.html

        # Parse HTML with Beautiful Soup
        hi_res_img_soup = BeautifulSoup(full_image, 'html.parser')

        all_hi_res_img = hi_res_img_soup('img', class_='wide-image')
        img_string = i.h3.text + str('.png')
        img_url = 'https://astrogeology.usgs.gov' + all_hi_res_img[0]['src']
        hemi_image_urls.append({"title": i.h3.text, "img_url": img_url})

        response = requests.get(img_url, stream=True)
        with open(img_string, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        Image(url=img_string)

        # Store scrapped data
    mars_data['Hemisphere_Description'] = hemi_image_urls

    return mars_data
