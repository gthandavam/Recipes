import urllib
import codecs

prefix = 'http://visualrecipes.com/'

if __name__ == '__main__':
	f_imgs = open('data/all_imgs', 'r')

	for img in f_imgs.readlines():
		img = img.rstrip('\n')
		img = img.strip()
		urllib.urlretrieve(prefix+img, './data/'+img)
