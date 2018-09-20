
# coding: utf-8

# In[79]:


from bs4 import BeautifulSoup as bs
import requests
import urllib.request
from splinter import Browser
import pandas as pd


def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[38]:


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # ## To scrape first article on first page

    # In[50]:


    article = soup.find('li', class_='slide')


    # In[56]:


    news_title = article.find('h3').text
    news_p = article.find('div', class_='article_teaser_body').text


    # ## Scrape JPL site for full size version of the featured image

    # In[57]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # In[58]:


    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # In[67]:


    img = soup.find('article', class_='carousel_item')

    featured_image_url = 'https://www.jpl.nasa.gov' + img['style'].split("'")[1]


    # ## Scrape Mars weather Twitter account for most recent tweet

    # In[74]:


    url = 'https://twitter.com/marswxreport?lang=en'


    # In[77]:


    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # In[78]:


    mars_weather = soup.find('p', class_='tweet-text').text


    # ## Scrape Mars fact table

    # In[81]:


    url = 'http://space-facts.com/mars/'


    # In[84]:


    table = pd.read_html(url)
    html_table = table[0].to_html()


    # ## Scrape USGS Astrogeology site for high res imges of each fo Mars' hemispheres

    # In[109]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[110]:


    browser.visit(url)


    # In[111]:


    hemisphere_image_urls = []
    hemispheres = ['Cerberus Hemisphere','Schiaparelli Hemisphere',
                'Syrtis Major Hemisphere','Valles Marineris Hemisphere']
    for h in hemispheres:
        browser.click_link_by_partial_text(h)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.findAll('dd')[1].find('a')['href']
        hemisphere_image_urls.append({'title':h, 'img_url':img_url})
        browser.click_link_by_partial_text('Back')
    print('Done Scraping')
    return {'news_title':news_title, 'news_p':news_p, 
    'featured_image_url':featured_image_url, 'mars_weather':mars_weather,
    'html_table':html_table, 'hemisphere_image_urls':hemisphere_image_urls}
