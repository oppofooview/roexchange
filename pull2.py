from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import re
import time
import traceback

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(options=opts)
nowtime = int(time.time()) 
baseurl = 'https://www.romwiki.net/items?type=card&page={}'
max_pages = 18
#max_pages = 1
for i in range(1, max_pages+1):
    try: 
        url = baseurl.format(i)
        browser.get(url)
        cards = browser.find_elements_by_css_selector('.columns.is-mobile')
        for c in cards:
            name = c.find_element_by_css_selector('.card-name').text
            info = c.find_element_by_css_selector('.card-info').find_elements_by_tag_name('tr')
            effects = ','.join([x.text.replace(u"\uff0b", '+').replace('\n', '') for x in info[0].find_elements_by_tag_name('td')[1:]])
            unlock = ','.join([x.text.replace(u"\uff0b", '+').replace('\n', '') for x in info[1].find_elements_by_tag_name('td')[1:]])
            deposit = ','.join([x.text.replace(u"\uff0b", '+').replace('\n', '') for x in info[2].find_elements_by_tag_name('td')[1:]])
            source = info[3].find_elements_by_tag_name('td')[1].text
            slot = info[4].find_elements_by_tag_name('td')[1].text
            print('{}|{}|{}|{}|{}|{}'.format(name, effects, unlock, deposit, source, slot))
            #print(name,effects,source,slot)
            # c.text.encode('raw_unicode_escape')
      #m = re.search('Price: (.*) ', info)
      #m2 = re.search('Volume: (.*) ', info)

    except:
        print('Error encountered during scraping')
        traceback.print_exc()
      
    #html = browser.page_source
    #print(html)


