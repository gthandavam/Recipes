__author__ = 'gt'
import commands
from BeautifulSoup import BeautifulSoup
import codecs

encoding = 'utf-8'
ctr = open('BlockSplit.csv','w')
files = commands.getoutput('find /Users/gt/CookScrap/VR/transitions-2-pretty-V -type f ')

idx = 0
for htmlf in files.rstrip().split('\n'):
  print 'Processing ' + str(idx + 1) + ' ' + htmlf
  idx += 1
  f = codecs.open(htmlf, 'r', encoding)
  ret = [] #empty list
  text = ''
  for line in f.readlines():
    line = line.replace('\n', ' ')
    text += line
  f.close()

  soup = BeautifulSoup(text)
  tables = soup.findAll('table')



  #first table contains the steps
  trs = tables[0].findAll('tr')
  #accounting for one th row
  ctr.write(str(len(trs) - 1) + ',' + htmlf )
  ctr.write('\n')


ctr.close()


