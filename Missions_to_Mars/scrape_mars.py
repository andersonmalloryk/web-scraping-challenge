def scrape_info():
    import pandas as pd
    import requests
    import pymongo
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup
    from splinter import Browser

    #Pull the featured_stories

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    sidebar = soup.find('div', class_="col-md-12")
    categories = sidebar.find_all('div')

    titles = []
    paragraphs = []

    for category in categories:
        title = getattr(category.find('div', class_='content_title'), 'text', None)
        titles.append(title)
        paragraph = getattr(category.find(
            'div', class_='article_teaser_body'), 'text', None)
        paragraphs.append(paragraph)
        if (title and paragraph):
            # Print results
            print('-------------')
            print(title)
            print(paragraph)

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # print(soup)

    featured_image_url = soup.find('a', class_="showimg fancybox-thumbs")['href']
    featured_image_url = image_url + featured_image_url
    print(featured_image_url)

    browser.quit()

    featured_stories = []

    #set up the dictionary to be inserted into MongoDb
    for i, j in zip(titles, paragraphs):
        featured_stories.append({"title": i, 'story': j})

    # pull the featured image
    facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(facts_url)
    # tables

    #return is a list of dataframes for any tabular data that Pandas found
    type(tables)

    #slice off dataframes that we want using normal indexing
    facts_df = tables[0]

    #drop single header rows
    facts_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    facts_df.head()

    facts_df.drop([0], inplace=True)

    facts_df.set_index('Mars - Earth Comparison', inplace=True)

    facts_df

    mars_profile_df = tables[1]
    mars_profile_df.columns = ['Mars', 'Planet Profile']

    mars_profile_df.set_index('Mars', inplace=True)
    mars_profile_df

    facts_html_table = facts_df.to_html()
    profile_html_table = mars_profile_df.to_html()

    profile_html_table.replace('\n', '')
    facts_html_table.replace('\n', '')

    # Pull the hemisphere images
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    astro_url = 'https://marshemispheres.com/'
    browser.visit(astro_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    enhanced_urls = []
    titles = []

    results = soup.find_all('div', class_='item')

    #print(results)

    #borrowed from Mike H -- because I was getting more content than needed.

    for result in results:
        if result.find('h3'):
            title = result.find('h3').text
            titles.append(title)
            print(title)
        if result.find('a'):
            link = result.find('a')
            href = link['href']
            enhanced_url = astro_url + href
            enhanced_urls.append(enhanced_url)
            print(enhanced_url)

    #iterate over the link list using .click() to pull the high res image url from each link

    image_urls = []

    for enhanced_url in enhanced_urls:
        browser.visit(enhanced_url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

    #browser.links.find_by_partial_text('Sample').click()

        link = soup.body.find_all('img', class_='wide-image')
        src = link[0]['src']
        image_url = astro_url + src
        image_urls.append(image_url)
        print(image_url)

    browser.quit()

    #set up the dictionary to be inserted into MongoDb
    hemisphere_image_urls = []
    for i, j in zip(titles, image_urls):
        hemisphere_image_urls.append({"title": i, 'image_url': j})

    # print(hemisphere_image_urls)

return featured_stories
return featured_image_url
return hemisphere_image_urls
