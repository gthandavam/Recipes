import urllib2
from BeautifulSoup import BeautifulSoup
import string
import subprocess
import codecs

#import pdb
#pdb.set_trace()

prefix = 'http://visualrecipes.com/'


def get_ingredients(url):
	soup = BeautifulSoup(urllib2.urlopen(prefix+url).read())
	ul_ing = soup('ul',{'class' : 'ingredients'})	
	
	return ul_ing[0]('li')
	

if __name__ == "__main__":

	#f = open('urlList-test', 'r')
	f = open('urlList', 'r')
	#all_images = dict()

	r_cnt = 1;
	
	for url in f.readlines():

		name = url.split('/')[-2]
		print 'recipe ' + str(r_cnt) + ': ' + name + '\n'
		r_cnt += 1

		#cmd = ['mkdir', '-p', 'data/'+name]
		#ret = subprocess.call(cmd)


		f_ing = codecs.open('data/'+name+'/ingredients', 'w', 'utf-8')

		try:

			ings = get_ingredients(url)

			for ing in ings:
				f_ing.write(ing.text+'\n')

		except IndexError:
			print name + ' different ingredient'
			continue

		#f_img = codecs.open('data/'+name+'/images', 'w', 'utf-8')
		#soup = BeautifulSoup(urllib2.urlopen(prefix + url).read())
		#
		#f_steps = codecs.open('data/'+name+'/steps', 'w', 'utf-8')
		#steps = soup('div', {'class' : 'step'})

	#	i = 0
	#	for step in steps:
	#		i += 1

		#	img_recipe_steps = step('div', { 'class' : 'img-recipe-steps'})


		#	for img_recipe_step in img_recipe_steps:

		#		a_tags = img_recipe_step('a')

		#		for a_tag in a_tags:
		#			#print a_tag['href']
		#			f_img.write(a_tag['href'])
		#			f_img.write('\n')
		#		
		#			#bookkeeping
		#			if( a_tag['href'] in all_images ):
		#				print 'dupe image:' + a_tag['href'] + '\n'
		#				all_images[a_tag['href']] += 1
		#			else :
		#				all_images[a_tag['href']] = 1


		#	step_contents = step('div', {'class': 'step-content'})

		#	for step_content in step_contents:
		#		narrations = step_content('p')
		#		for narration in narrations:
		#			f_steps.write( "XXXGTXXX step " + str(i) + "\n")
		#			f_steps.write(narration.text + '\n')

		##closing the files after iterating thru steps
		#f_img.close()
		#f_steps.close()


#	f_imgs = codecs.open('data/all_imgs', 'w', 'utf-8')
#
#	for key in all_images.keys():
#		f_imgs.write(key+'\n')

		
