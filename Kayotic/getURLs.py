import urllib2
from BeautifulSoup import BeautifulSoup
import string
import codecs
import pdb
pdb.set_trace()

encode = 'utf-8'
prefix = 'http://www.kayotic.nl'
if __name__ == "__main__":

	f = codecs.open('urlList','w', encode)

	url = 'http://www.kayotic.nl/blog/visual-index?vi_orderby=date&vi_per_page=60&vi_page='
	for i in range(1,11):
		soup = BeautifulSoup(urllib2.urlopen(url + str(i)).read())
		lis = soup('div', {'id':'content'})[0]('div', {'class':'content'})[0]('div', {'class':'article'})[0]('ul',{'class' : 'vi-index'})[0]('li')
		for li in lis:
			a_tags = li('a')
			for a_tag in a_tags:
				f.write(a_tag['href']+'\n')


	f.close()
			
	
