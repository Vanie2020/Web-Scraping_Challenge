
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
    featured_image_url = "https://spaceimages-mars.com/{img_url}"

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
    idx_df

    #Save table string
    mars_df = df.to_html(classes = 'table table-striped')


    # ### Mars Hemispher

    # Navigate to the page
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)

    hemisphere_html = browser.html
    soup = bs(hemispere_html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://marshemispheres.com/'

    for item in items: 
    
        title = item.find('h3').text
        
        image_url = item.find('a', class_='itemLink product-item')['href']

        browser.visit(hemispheres_main_url + image_url)

        image_html = browser.html

        soup = bs( image_html, 'html.parser')

        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})
        
        

    browser.quit()

    new_dict = {
        "news_t": news_title,
        "news_p": news_paragraph,
        "mars_f": featured_image_url,

    }

    return new_dict




