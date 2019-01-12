from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from declare_db import Base, Info 
import time
import traceback

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(options=opts)

urlmap = {
'Crystal Mirror': 'https://poporing.life/?search=crystal%20mirror',
'Soft Feather': 'https://poporing.life/?search=soft%20feather',
'Orc Claw': 'https://poporing.life/?search=orc%20claw',
'Bell': 'https://poporing.life/?search=bell',
'Rose Quartz': 'https://poporing.life/?search=rose%20quartz',
'Antenna': 'https://poporing.life/?search=antenna',
'Cursed Ruby': 'https://poporing.life/?search=cursed%20ruby',
'Raccoon Leaf': 'https://poporing.life/?search=raccoon%20leaf',
'Bloody Rune': 'https://poporing.life/?search=bloody%20rune',
'Light Granule': 'https://poporing.life/?search=light%20granule',
'Wrapping Lace': 'https://poporing.life/?search=wrapping%20lace',
'Star Crumb': 'https://poporing.life/?search=star%20crumb',
'Pearl': 'https://poporing.life/?search=pearl',
'Parts': 'https://poporing.life/?search=parts',
'Heroic Emblem': 'https://poporing.life/?search=heroic%20emblem',
'Dragon Scale': 'https://poporing.life/?search=dragon%20scale',
'Fabric': 'https://poporing.life/?search=fabric',
'Four Leaf Clover': 'https://poporing.life/?search=four%20leaf%20clover',
'Emperium': 'https://poporing.life/?search=emperium',
}

engine = create_engine('sqlite:///exchange.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

nowtime = int(time.time()) 
for key, value in urlmap.items():
    print(key, value)
    '''if key != 'Dragon Scale':
        continue
    browser.get(value)
    '''
    try: 
      info = browser.find_elements_by_css_selector('.d-flex.flex-column')[-1].text
      print(info)
      m = re.search('Price: (.*) ', info)
      m2 = re.search('Volume: (.*) ', info)

      price = m.group(1).replace(',', '')
      volume = m2.group(1).replace(',', '') 
      print('Price is {}'.format(price))
      print('Volume is {}'.format(volume))
      newinfo = Info(item_name=key, timestamp=nowtime, price=int(price), volume=int(volume))
      session.add(newinfo)
      session.commit()
    except:
      print('Price or volume was not found')
      traceback.print_exc()
      newinfo = Info(item_name=key, timestamp=nowtime, price=None, volume=None)
      session.add(newinfo)
      session.commit()

    #print(info)
    #html = browser.page_source
    #print(html)
    #break


