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
baseurl = 'https://www.roguard.net/db/cards/?page={}'
for i in range(1, 15):
    try: 
        url = baseurl.format(i)
        browser.get(url)
        info = browser.find_elements_by_css_selector('.table.text-center')[-1]
        cards = info.find_elements_by_tag_name('a')
        for c in cards:
            print(c.text.replace(u"\u2605", ' star ').lower().replace(' ', '_')) 
            # c.text.encode('raw_unicode_escape')
      #m = re.search('Price: (.*) ', info)
      #m2 = re.search('Volume: (.*) ', info)

    except:
        print('Price or volume was not found')
        traceback.print_exc()
      
    #html = browser.page_source
    #print(html)


