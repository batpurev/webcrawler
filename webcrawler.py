from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import validators
import os
import asyncio
from playwright.async_api import async_playwright


# Use sync version of Playwright
def get_links(page_url):
    global pages
    valid=validators.url(page_url)
    if valid==True:
        #with async_playwright() as p:
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch()

            # Open a new browser page
            page = browser.new_page()
            #page.setDefaultNavigationTimeout(0) 
            # Open our test file in the opened page
            page.goto(page_url)
            page_content = page.content()

            # Process extracted content with BeautifulSoup
            soup = BeautifulSoup(page_content,features="lxml")
            
            # start new TMP array
            pages_tmp = set()
           
            for link in soup.find_all("a"):
                if "href" in link.attrs:
                  if link.attrs["href"] not in pages:
                    new_page = link.attrs["href"]
                    # Check if url is valid or not. (maybe internal if it is NOT valid).
                    valid123=validators.url(new_page)
                    if valid123==True:
                        # Check if it starts with our base_url
                        if new_page.startswith(base_url): # this is within our target site so we will Crawl it. If external we are not crawling
                            if new_page not in pages:
                                #pages.add(new_page) # we add it into our list.
                                pages_tmp.add(new_page)
                                pages.add(new_page)
                    else:
                        # NOT valid is maybe cause it is internal URL such as /homepage so we prefix it with base_url 
                        new_page = base_url + new_page
                        # now check if the URL is valid
                        valid123456=validators.url(new_page)
                        if valid123456==True:
                            if new_page not in pages: 
                                #pages.add(new_page) # we add it into our list.
                                pages_tmp.add(new_page)
                                pages.add(new_page)
                    #print(new_page)
                    #pages.add(new_page)
                    #get_links(new_page)

            # Close browser
            browser.close()
    else:
        print('invalid URL: ' + page_url)
    
    # call recursion if new pages found otherwise end it
    if len(pages_tmp) > 0:
        # loop through all new pages
        for ppp in pages_tmp:
            # add this page into pages as it will be visited now
    #        pages.add(ppp)
            get_links(ppp)
    #print(pages_tmp)
    #pages.add(pages_tmp)

global base_url
global pages
pages = set()

base_url='https://www.yourdomain.com/' # MUST include trailing slash
pages.add(base_url)

start_url = "http://www.yourdomain.com/some/post/with/as/many/links/as/possible/"
get_links(start_url)

# print all uniqui URLs found within BASE URL.
print(pages)



