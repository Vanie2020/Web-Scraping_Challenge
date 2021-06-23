import datetime as dt

#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    #pointing to the directory where chromedriver exists
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)


    # Open browser to NASA Mars News Site
    browser.visit('https://redplanetscience.com/')

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    # ### JPL Mars Space Images - Featured Image

    url_image = "https://spaceimages-mars.com"
    browser.visit(url_image)


    # Assign the HTML content and use BS
    img_html = browser.html
    soup = bs(img_html,'html.parser')



    # Find current featured url image
    img_result = soup.find('img', class_="headerimage fade-in")['src']

    img_url = img_result.replace("background-image: url('","").replace("');","")
    featured_image = f"https://spaceimages-mars.com/{img_url}"

    # ### Mars Facts

    # Collect the tables  
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)

    # Parse the URL
    tables = pd.read_html(facts_url)

    # Find in lists of dataframes
    df = tables[1]
    df.columns = ["Description","Value"]
    idx_df = df.set_index("Description")
    

    #Save table string
    mars_facts = idx_df.to_html(classes = 'table table-striped')

    # ### Mars Hemispher

    # Navigate to the page
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)

    hemisphere_html = browser.html
    soup = bs(hemisphere_html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemispheres_list_of_dicts = []

    hemispheres_main_url = 'https://marshemispheres.com/'

    for item in items: 
    
        title = item.find('h3').text
        
        image_url = item.find('a', class_='itemLink product-item')['href']

        browser.visit(hemispheres_main_url + image_url)

        image_html = browser.html

        soup = bs( image_html, 'html.parser')

        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        hemispheres_list_of_dicts.append({"title" : title, "img_url" : image_url})


    scraped_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image,
        "facts": mars_facts,
        "hemispheres": hemispheres_list_of_dicts,
        "last_modified": dt.datetime.now()
    }
    browser.quit()


    return scraped_data




