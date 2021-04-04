#!/usr/bin/env python
# coding: utf-8

# # Scraping with Pandas

# In[ ]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests


# ### NASA Mars News
# Scrape the Mars News Site (url) to collect the latest News Titles and Paragraph text. 
# Save these to variables to use them later.
# - Set up URL
# - Retrieve page with splinter
# - Examine the results, determine element that contains the title and paragraph
# - Set to variables 
# - quit browser

# In[ ]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://redplanetscience.com/'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

featured = soup.find('div', class_="list_text")
featured_title = featured.find('div', class_='content_title').text
featured_paragraph = featured.find('div', class_='article_teaser_body').text


# In[ ]:


browser.quit()


# ### JPL Mars Space Images - Featured Image
# Visit the Featured Space Image site (image_url)to collect images.
# Use splitner to navigate to the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# - Set up splinter
# - Find content needed
# - Save content to a variable
# - Quit the browser

# In[ ]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

image_url = 'https://spaceimages-mars.com/'
browser.visit(image_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

featured_image_url = soup.find('a', class_="showimg fancybox-thumbs")['href']

featured_image_url = image_url + featured_image_url


# In[ ]:


browser.quit()


# ### Mars Facts
# Visit the Mars Facts webpage (facts_url) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. Use Pandas to convert the data to a HTML table string.
# - go to the URL
# - pull the tables using read_html
# - set the tables to data frames pulling each one using it's index
# - read them back to HTML for Flask

# In[ ]:


facts_url = 'https://galaxyfacts-mars.com/'


# In[ ]:


tables = pd.read_html(facts_url)
tables


# In[ ]:


type(tables)


# In[ ]:


facts_df = tables[0]


# In[ ]:


#drop single header rows
facts_df.columns = ['Mars - Earth Comparison','Mars','Earth']
facts_df.head()


# In[ ]:


facts_df.drop([0], inplace=True)


# In[ ]:


facts_df.set_index('Mars - Earth Comparison',inplace=True)


# In[ ]:


facts_df


# In[ ]:


mars_profile_df = tables[1]
mars_profile_df.columns = ['Mars','Planet Profile']


# In[ ]:


mars_profile_df.set_index('Mars',inplace=True)
mars_profile_df


# In[ ]:


facts_html_table = facts_df.to_html()
profile_html_table = mars_profile_df.to_html()


# In[ ]:


profile_html_table.replace('\n', '')
facts_html_table.replace('\n', '')


# ### Mars Hemispheres
# Visit the astrogeology site (astro_url) to obtain high resolution images for each of Mars's hemispheres.
# 
# - Click each of the links to the hemispheres in order to find the image url to the full resolution image.
# - Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
# - Use a Python dictionary to store the data using the keys img_url and title.
# - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[ ]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

astro_url = 'https://marshemispheres.com/'
browser.visit(astro_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

enhanced_urls = []
enhanced_titles = []

results = soup.find_all('div', class_='item')


# In[ ]:


#borrowed from Mike H -- because I was getting more content than needed.

for result in results:
    if result.find('h3'):
        title = result.find('h3').text
        enhanced_titles.append(title)
        print(title)
    if result.find('a'):
        link = result.find('a')
        href = link['href']
        enhanced_url = astro_url + href
        enhanced_urls.append(enhanced_url)
        print(enhanced_url)


# In[ ]:


image_urls = []

for enhanced_url in enhanced_urls:
    browser.visit(enhanced_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    link = soup.body.find_all('img', class_='wide-image')
    src = link[0]['src']
    image_url = astro_url + src
    image_urls.append(image_url)
    print(image_url)


# In[ ]:


browser.quit()


# In[ ]:


scrape_content = {"featured_title": featured_title,
                 "featured_paragraph": featured_paragraph,
                 "featured_image": featured_image_url,
                 "hemisphere_title": enhanced_titles,
                 "hemisphere_images": image_urls}

