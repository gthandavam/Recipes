import urllib2
from BeautifulSoup import BeautifulSoup
import string
import pdb
pdb.set_trace()

prefix = 'http://step-by-step-cook.co.uk/'

if __name__ == "__main__":

	f = open('urlList','w')

	url = 'http://step-by-step-cook.co.uk/overview/'
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	
	links = soup('div', {'id' : 'content'})[0]('table')[0]('a')	

	for link in links:
		f.write(link['href'] + '\n')

	f.close()
	
