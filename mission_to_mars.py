
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def init_browser():
    # NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


def scrape():
    # Set up connection to chrome driver.
    browser = init_browser()


    
    #-----------------------------------------------------------------------------

    #Sets up visit to twitter.
    TwitterMarsUrl='https://twitter.com/marswxreport?lang=en'
    browser.visit(TwitterMarsUrl)
    time.sleep(7)

    #Scrolls down 3000.This has to be done because the data we want hasn't populated yet.
    browser.execute_script("window.scrollTo(0, 3000);")
    time.sleep(2)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    spanned=soup.find_all('span')
    
    for span in spanned:
        if 'InSight sol ' in span.text:
            mars_weather=span.text
            break
            
    #-----------------------------------------------------------------------------
    
    #Visits the news page to retrieve latest news title/paragraph.
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    #Converts html to BS object.
    time.sleep(4)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #-----------------------------------------------------------------------------

    #Gets the latest News Article with their title and paragraph.
    LatestArt=soup.find('li',class_="slide")

    LatTitle = LatestArt.find('div',class_='content_title').text
    LatPara = LatestArt.find('div',class_='article_teaser_body').text

    #-----------------------------------------------------------------------------

    #Visits mars spaces image part of the site.
    FeatureMarsUrl='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(FeatureMarsUrl)
    time.sleep(4)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    FeatElement=soup.find('div',class_='carousel_items')


    #-----------------------------------------------------------------------------

    #Retrieves the String of the featured space image and joins the strings to get the correct url.

    StartUrl='https://www.jpl.nasa.gov'


    #-----------------------------------------------------------------------------
    #Cleans ups the string element to retrieve the correct ending url for image.
    SplitUp=FeatElement.article['style'].split('\'')
    EndImgUrl=SplitUp[1]

    featured_image_url = StartUrl+EndImgUrl
    


    #-----------------------------------------------------------------------------
    #Grabs the martian facts table.
    MarsFacts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(MarsFacts_url)


    #-----------------------------------------------------------------------------
    #Saves table of interest as an html string.
    FactsTable=tables[0].rename(columns={0: 'Type', 1: 'Fact'})
    FactsTable.set_index('Type',inplace=True)
    MartianHTML_table = FactsTable.to_html(classes='data', header="true")

    #-----------------------------------------------------------------------------

    #Creates a list of dictionaries of each hemisphere of Mars.
    
    HemiUrl ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    ListsOfHemi=['Cerberus','Schiaparelli','Syrtis','Valles']
    HemiImgList = []

    for Hemi in ListsOfHemi:
        browser.visit(HemiUrl)
        time.sleep(4)
        browser.click_link_by_partial_text(Hemi)
        soup = BeautifulSoup(browser.html, 'html.parser')
        imgurl=soup.find('a',text='Sample')['href']
        HemiImgList.append(imgurl)

    #-----------------------------------------------------------------------------
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": HemiImgList[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": HemiImgList[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": HemiImgList[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": HemiImgList[3]}
    ]
    #-----------------------------------------------------------------------------
    dictData= {
                'LatTitle':LatTitle,
                'LatPara':LatPara,
                'featured_image_url':featured_image_url,
                'mars_weather':mars_weather,
                'MartianHTML_table':MartianHTML_table,
                'hemisphere_image_urls':hemisphere_image_urls
        }
    
    return dictData