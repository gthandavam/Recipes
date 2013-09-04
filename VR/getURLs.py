import urllib2
from BeautifulSoup import BeautifulSoup
import string
import pdb
pdb.set_trace()

prefix = 'http://visualrecipes.com/'

if __name__ == "__main__":

	f = open('urlList','w')

	end = 0
	for i in range(61):
		url = 'http://visualrecipes.com/recipes/P'
		soup = BeautifulSoup(urllib2.urlopen(url + str(end)).read())
		recipe_headlines = soup('h2', {'class' : 'sIFR-ignore'})	

		for recipe_headline in recipe_headlines:
			a_tags = recipe_headline('a')

			for a_tag in a_tags:
				f.write(a_tag['href'])
				f.write('\n')
		
		end = end + 10


			
	
