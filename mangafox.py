import requests, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




## Creates a filename
def makeFileName(browser, page):
    chapter = browser.find_element_by_class_name('reader-header-title-2')
    chapterStr = chapter.text
    title = browser.find_element_by_class_name('reader-header-title-1')
    titleStr = title.find_element_by_tag_name('a').text
    return os.path.join(titleStr, f'{chapterStr} pg{page}.jpg')


## Downloads a page
def downloadPage(browser, page):
    imageElement = browser.find_element_by_class_name('reader-main-img')
    imageUrl = imageElement.get_attribute('src')
    while imageUrl.endswith('loading.gif'):
        imageElement = browser.find_element_by_class_name('reader-main-img')
        imageUrl = imageElement.get_attribute('src')
    res = requests.get(imageUrl)
    res.raise_for_status
    with open(makeFileName(browser, page), 'wb') as imageFile:
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)


## Finds the inputted manga on manga fox, returns the exact title and url of the first chapter
def findManga():
    choice = input('Enter a full or partial manga title as seen on Manga Fox. ')
    browser = webdriver.Chrome()
    browser.get('http://fanfox.net/')
    searchBar = browser.find_element_by_id('fastsearch')
    searchBar.send_keys(choice)
    searchBar.send_keys(Keys.ENTER)
    mangaLink = browser.find_element_by_partial_link_text(choice)
    mangaLink.click()
    chapter1 = browser.find_element_by_partial_link_text('Ch.001')
    url = chapter1.get_attribute('href')
    title = browser.find_element_by_class_name('detail-info-right-title-font').text
    browser.quit()
    return [url, title]



## Version 1 - Mangafox started blocking the next button with ads
manga = findManga()
url = manga[0]
title = manga[1]
confirm = input(f'Do you want to download {title}? Enter yes or no. ')
if confirm == 'yes':
    getMore = True
    page = 1
    browser = webdriver.Chrome()
    browser.get(url)
    os.makedirs(title, exist_ok = True) 
    downloadPage(browser, page)
    while getMore == True:
        try:
            nextPage = browser.find_element_by_link_text('>')
            nextPage.click()
            page+=1
            downloadPage(browser, page)
        except:
            try:
                nextPage = browser.find_element_by_link_text('Next Chapter')
                nextPage.click()
                page = 1
                downloadPage(browser, page)
            except:
                getMore = False
    browser.quit()
else:
    print('Goodbye')
