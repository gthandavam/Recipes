import urllib2
from BeautifulSoup import BeautifulSoup
import string
import subprocess
import codecs

import HTMLParser

encode = 'utf-8'
prefix = 'http://www.kayotic.nl'

all_images = dict()
h = HTMLParser.HTMLParser()

#Demonstration of python LEGB rules in the usage of name variable
#http://stackoverflow.com/questions/291978/short-description-of-python-scoping-rules

def get_ingredients(p_tags, i):
	f_ings = codecs.open('data/'+name+'/ingredients', 'w', encode)
	for idx in range(i, len(p_tags)):
		if ( hasattr(p_tags[idx], 'strong') and hasattr(p_tags[idx].strong, 'text') and p_tags[idx].strong.text == 'Directions:' ):
			get_steps_and_images(p_tags, idx+1)
			break
		else :
			f_ings.write(h.unescape(p_tags[idx].text)+'\n')

def get_steps_and_images(p_tags, i):
	f_steps = codecs.open('data/'+name+'/steps', 'w', encode)
	ctr = 1
	for idx in range(i, len(p_tags)):
		f_steps.write('Step ' + str(ctr) + '\n')
		f_steps.write( h.unescape(p_tags[idx].text) + '\n')
		if( hasattr(p_tags[idx], 'a') and hasattr(p_tags[idx].a, 'img') and hasattr(p_tags[idx].a.img, 'src') ):
			if( p_tags[idx].a.img['src'] in all_images ):
				print 'dupe image:' + p_tags[idx].a.img['src'] + '\n'
				all_images[p_tags[idx].a.img['src']] += 1
			else :
				all_images[p_tags[idx].a.img['src']] = 1 

			f_steps.write(p_tags[idx].a.img['src']+'\n')

		ctr += 1

def get_ings_steps_and_images(soup):
	p_tags = soup('div', {'id' : 'wrapper'})[0]('div', {'class' : 'container'})[0]('div', {'id' : 'content'})[0]('div', {'class':'article'})[0]('p')

	i = 0
	for i in range(len(p_tags)):
		if ( hasattr(p_tags[i], 'strong') and hasattr(p_tags[i].strong, 'text') and p_tags[i].strong.text == 'Ingredients:' ):
			get_ingredients(p_tags, i+1)	
			break

if __name__ == "__main__":

	f_url = open('urlList', 'r')

	for url in f_url.readlines():
		url = url.rstrip('\n')
		url = url.strip()

		soup = BeautifulSoup(urllib2.urlopen(url).read())

		name = url.split('/')[-1]
		
		cmd = ['mkdir', '-p', 'data/'+name]
		ret = subprocess.call(cmd)
	
		print 'processing ' + name + '\n'	
		get_ings_steps_and_images(soup)

	f_images = open('data/all_images', 'w')
	
	for key in all_images.keys():
		f_images.write(key+'\n')
