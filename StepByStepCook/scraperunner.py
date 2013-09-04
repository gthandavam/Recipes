import urllib2
from BeautifulSoup import BeautifulSoup
import string
import subprocess
import codecs
import sys #sys imported for e.format()

encode = 'latin-1'

prefix = 'http://step-by-step-cook.co.uk'
#http://step-by-step-cook.co.uk//mains/pizza/ - not the same as
#http://step-by-step-cook.co.uk/mains/pizza/
#server was not handling the case when / is repeated

def get_ingredients(soup, name):
    f_ings = codecs.open('data/' + name + '/ingredients', 'w', encode)
    trs = soup('div' , {'id':'content'})[0]('table')[1]('tr')
    for tr in trs:
        tds = tr('td')        
        ing_line = ''
        for td in tds:
            ing_line += '  ' + str(td.text)
        f_ings.write(ing_line + '\n')
        
    f_ings.close()
            
def get_instructions(soup, name):
    trs = soup('div' , {'id':'content'})[0]('table')[2]('tr')
    
    #Opening the file after ensuring that there is no IndexError
    f_insts = codecs.open('data/' + name + '/steps', 'w', encode)
    
    cnt = 1
    
    for tr in trs:
        tds = tr('td')
        f_insts.write('step ' + str(cnt) + '\n')
        f_insts.write(tds[1].text + '\n')
        f_insts.write(tds[0]('img')[0]['src'] + '\n')
        all_images[tds[0]('img')[0]['src']] = 1
        cnt +=1
        
    f_insts.close()

if __name__ == "__main__":

	#f = open('urlList-test', 'r')
	f = codecs.open('urlList', 'r', encode)
	all_images = dict()

	r_cnt = 1;
	
	for url in f.readlines():
		url = url.rstrip('\n')
		url = url.strip()
		name = url.split('/')[-2]
		print 'recipe ' + str(r_cnt) + ': ' + name + '\n'
		r_cnt += 1
		
		cmd = ['mkdir', '-p', 'data/' + name]
		ret = subprocess.call(cmd)

		soup = BeautifulSoup(urllib2.urlopen(prefix + url).read())
		
		try:
		    #get_ingredients(soup, name)
		    get_instructions(soup, name)
		except IndexError as e:
		    print "IndexError " + name
		    continue
		    
	f_imgs = open('data/all_images', 'w')
	
	for key in all_images.keys():
	    f_imgs.write(key+'\n')
	    
	f_imgs.close()