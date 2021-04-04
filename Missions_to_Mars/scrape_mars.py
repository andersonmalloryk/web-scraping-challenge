
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests

def scrape_info():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured = soup.find('div', class_="list_text")
    featured_title = featured.find('div', class_='content_title').text
    featured_paragraph = featured.find('div', class_='article_teaser_body').text

    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('a', class_="showimg fancybox-thumbs")['href']

    featured_image_url = image_url + featured_image_url

    browser.quit()

    facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(facts_url)
    tables

    type(tables)

    facts_df = tables[0]

    facts_df.columns = ['Mars - Earth Comparison','Mars','Earth']
    facts_df.head()

    facts_df.drop([0], inplace=True)

    facts_df.set_index('Mars - Earth Comparison',inplace=True)

    facts_df

    mars_profile_df = tables[1]
    mars_profile_df.columns = ['Mars','Planet Profile']

    mars_profile_df.set_index('Mars',inplace=True)
    mars_profile_df

    facts_html_table = facts_df.to_html()
    profile_html_table = mars_profile_df.to_html()

    profile_html_table.replace('\n', '')
    facts_html_table.replace('\n', '')

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    astro_url = 'https://marshemispheres.com/'
    browser.visit(astro_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    enhanced_urls = []
    enhanced_titles = []

    results = soup.find_all('div', class_='item')

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

    browser.quit()

    scrape_content = {"featured_title": featured_title,
                    "featured_paragraph": featured_paragraph,
                    "featured_image": featured_image_url,
                    "hemisphere_title": enhanced_titles,
                    "hemisphere_images": image_urls}
    
    return scrape_content

