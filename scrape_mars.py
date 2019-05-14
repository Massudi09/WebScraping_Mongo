# Import Dependecies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
mars = {}

# NASA Mars News
def marsNews():
    try: 
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        newsTitle = soup.find('div', class_='content_title').find('a').text
        newsP = soup.find('div', class_='article_teaser_body').text
        mars['news_title'] = newsTitle
        mars['news_paragraph'] = newsP
        return mars

    finally:
        browser.quit()

# JPL Mars Space Images - Featured Image
def marsImage():

    try: 
        browser = init_browser()
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        html_image = browser.html
        soup = bs(html_image, 'html.parser')
        featured_image  = soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
        urlNasa = 'https://www.jpl.nasa.gov'
        featured_image_url = urlNasa + featured_image
        featured_image_url
        mars['featured_image_url'] = featured_image_url
        return mars

    finally:
        browser.quit()
        
# Mars Weather 
def marsWeather():

    try: 
        browser = init_browser()
        weatherUrl = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weatherUrl)
        htmlWeather = browser.html
        soup = bs(htmlWeather, 'html.parser')
        recentTweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        mars['recentTweet'] = recentTweet
        return mars

    finally:
        browser.quit()

# Mars Facts
def marsFacts():

    facts_url = 'http://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    marsInfo = table[0]
    marsInfo.columns = ['Metric','Value']
    marsInfo.set_index('Metric', inplace=True)
    data = marsInfo.to_html()
    mars['mars_facts'] = data
    return mars

# Mars Hemispheres
def marsHemispheres():

    try: 
        browser = init_browser()
        hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        marsHems_url = []
        links = soup.find_all("div", class_="item")

        for link in links:
            title = link.find("h3").text
            nextLink = link.find("div", class_="description").a["href"]
            imageLink = "https://astrogeology.usgs.gov" + nextLink
            browser.visit(imageLink)
            img_html = browser.html
            img_soup = bs(img_html, 'html.parser')
            url = "https://astrogeology.usgs.gov" + img_soup.find("img", class_="wide-image")["src"]
            marsHems_url.append({"title" : title, "img_url" : url})
        mars['marsHems_url'] = marsHems_url
        return mars

    finally:
        browser.quit()
