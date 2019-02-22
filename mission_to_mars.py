    #!/usr/bin/env python
    # coding: utf-8

    # In[19]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)


    # In[16]:

def scrape():
    # Set up connection to chrome driver.
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = init_browser()



    # In[63]:


    #Visits the news page to retrieve latest news title/paragraph.
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    #Converts html to BS object.
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[64]:


    #Gets the latest News Article with their title and paragraph.
    LatestArt=soup.find('li',class_="slide")

    LatTitle = LatestArt.find('div',class_='content_title').text
    LatPara = LatestArt.find('div',class_='article_teaser_body').text


    # In[65]:


    #Visits mars spaces image part of the site.
    FeatureMarsUrl='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(FeatureMarsUrl)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    FeatElement=soup.find('div',class_='carousel_items')


    # In[66]:


    #Retrieves the String of the featured space image and joins the strings to get the correct url.

    StartUrl='https://www.jpl.nasa.gov'

    #Cleans ups the string element to retrieve the correct ending url for image.
    SplitUp=FeatElement.article['style'].split('\'')
    EndImgUrl=SplitUp[1]

    featured_image_url = StartUrl+EndImgUrl
    


    # In[67]:


    #Sets up visit to twitter.
    TwitterMarsUrl='https://twitter.com/marswxreport?lang=en'
    browser.visit(TwitterMarsUrl)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[68]:


    mars_weather=soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    # In[31]:


    #Grabs the martian facts table.
    MarsFacts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(MarsFacts_url)


    # In[38]:


    #Saves table of interest as an html string.
    FactsTable=tables[0].rename(columns={0: 'Type', 1: 'Fact'})
    FactsTable.set_index('Type',inplace=True)
    MartianHTML_table = [FactsTable.to_html(classes='data', header="true")]


    # In[26]:


    #Creates a list of dictionaries of each hemisphere of Mars.

    HemiUrl ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    ListsOfHemi=['Cerberus','Schiaparelli','Syrtis','Valles']
    HemiImgList = []

    for Hemi in ListsOfHemi:
        browser.visit(HemiUrl)
        browser.click_link_by_partial_text(Hemi)
        soup = BeautifulSoup(browser.html, 'html.parser')
        imgurl=soup.find('a',text='Sample')['href']
        HemiImgList.append(imgurl)


    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": HemiImgList[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": HemiImgList[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": HemiImgList[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": HemiImgList[3]}
    ]

    dictData= {
                'LatTitle':LatTitle,
                'LatPara':LatPara,
                'featured_image_url':featured_image_url,
                'mars_weather':mars_weather,
                'MartianHTML_table':MartianHTML_table,
                'hemisphere_image_urls':hemisphere_image_urls
        }
    
    return dictData