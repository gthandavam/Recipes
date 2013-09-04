import urllib
import codecs


if __name__ == '__main__':
	f_imgs = open('data/all_images', 'r')

	ctr = 1	
	for img in f_imgs.readlines():
		img = img.rstrip('\n')
		img = img.strip()
		urllib.urlretrieve(img, './data/images/' + str(ctr) + '.jpg')
		ctr += 1
