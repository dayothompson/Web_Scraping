#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


import time
import warnings
warnings.filterwarnings('ignore')


# In[2]:


#pointing to the directory where chromedriver exists
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser("chrome", **executable_path, headless = False)


# In[3]:



# Visit Nasa news url through splinter module

url = "https://mars.nasa.gov/news/"
browser.visit(url)
time.sleep(5)


# In[4]:


# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


article = soup.find("div", class_='list_text')


# In[6]:


# # Retrieve the latest element that contains news title and news_paragraph
news_title = article.find("div", class_="content_title").text
news_p = article.find("div", class_ ="article_teaser_body").text

# # Display scrapped data 
print(news_title)
print(news_p)


# In[7]:


# Visit JPL Featured Space Image url through splinter module

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[8]:


# browser.click_link_by_partial_text('first image')

browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(5)


# In[9]:


browser.click_link_by_partial_text('more info')
time.sleep(5)


# In[10]:


# HTML Object
html_image = browser.html

# Parse HTML with Beautiful Soup
image_soup = BeautifulSoup(html_image, 'html.parser')


# In[11]:


image = image_soup.find('section', class_='content_page module')


# In[12]:


image_url = image_soup.find('img', class_='main_image')['src']

# In[13]:

featured_image_url = 'https://www.jpl.nasa.gov' + image_url
print(featured_image_url)




# In[14]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
time.sleep(5)


# In[15]:


# HTML Object
html_tweet = browser.html

# Parse HTML with Beautiful Soup
tweet_soup = BeautifulSoup(html_tweet, 'html.parser')
time.sleep(5)



# In[16]:


twitter = tweet_soup.find_all('span')
time.sleep(5)



# In[17]:



    
for tweet in twitter:
    if tweet.text != '' and 'InSight' in tweet.text:
        print(tweet.text)
        break


# In[18]:


# url = 'https://space-facts.com/mars/'


# In[19]:


df = pd.read_html('https://space-facts.com/mars')
profile = df[0]
profile.rename(columns={0: "", 1: "Mars Planet Profile"}, inplace=True)
profile.set_index("", inplace=True)



# In[20]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
time.sleep(5)


# In[21]:


all_html = browser.html

all_soup = BeautifulSoup(all_html, 'html.parser')


# In[22]:


all_links = all_soup.find_all('div', class_='description')



# In[23]:


hemisphere_image_urls = []

for i in all_links:
    hemisphere_image_urls.append({"title": i.h3.text, 
                                  "img_url": 'https://astrogeology.usgs.gov' + i.a['href']})


# In[24]:


print (json.dumps(hemisphere_image_urls, indent=4, separators=(',', ': ')))


# In[26]:


for i in all_links:
    print('------------------------------------------')
    print(i.h3.text)
    print('https://astrogeology.usgs.gov' + i.a['href'])
    browser.visit('https://astrogeology.usgs.gov' + i.a['href'])
    time.sleep(5)
    browser.click_link_by_partial_text('Open')
    time.sleep(5)


# In[ ]:





# In[ ]:





# In[ ]:




