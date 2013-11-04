__author__ = 'gt'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from nltk import word_tokenize
from nltk import pos_tag
from nltk import PorterStemmer

import random
import codecs
from pprint import pprint

stemmer = PorterStemmer()

###Parameters
testP           = 0.9 #rand >= testP for test sample
negativeP       = 0.5 # rand >= negativeP for negative sample
trainFile       = 'trainSamples.txt' #train samples generated and then used
testFile        = 'testSamples.txt'  # same for test samples
archiveLocation = '/Users/gt/CookScrap/VR/transitions-2-pretty-V'
encoding        = 'utf-8' #encoding per website
stopLimit       = 612 #dev parameter - to check the sanity of the whole process
blockSeparator  = ' #BLOCK# ' #separator for 2 blocks
labelSeparator  = ' #LABEL# ' # separates the block and the label
###

def train(sents, labels):
  ft_extractor,X = get_unigram_features(sents)
  clf            = svm.SVC()
  clf.fit(X,labels)
  return ft_extractor,clf

def test(sents, ft_extractor, clf):
  X = ft_extractor.transform(sents)
  y = clf.predict(X)
  return y

def evaluate(observed, expected):
  if len(observed) != len(expected):
    raise 'Number of observations != Number of experiments'

  ctr = 0
  for i in range(len(observed)):
    if observed[i] == expected[i]:
      ctr+=1
  return ctr

def filter_text(sent):
  b1, b2 = sent.split(blockSeparator)
  b2 = b2.rstrip()

  b1            = b1.lower()
  tokens        = word_tokenize(b1)
  pos_tags      = pos_tag(tokens)
  filtered_sent = ' '
  for pos_t in pos_tags:
    if pos_t[1] in ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB']:
      filtered_sent += stemmer.stem('1' + pos_t[0]) + ' '

  b2 = b2.lower()
  tokens = word_tokenize(b2)
  pos_tags = pos_tag(tokens)
  filtered_sent = ' '
  for pos_t in pos_tags:
    if pos_t[1] in ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB']:
      filtered_sent += stemmer.stem('2' + pos_t[0]) + ' '

  return filtered_sent

def get_unigram_features(sents):
  vec = CountVectorizer(min_df=1, tokenizer=word_tokenize,
                        preprocessor=filter_text )
  X   = vec.fit_transform(sents)
  return vec, X

def get_experiment_data(expFile):
  expF   = codecs.open(expFile, 'r',encoding)
  sents  = []
  labels = []

  for line in expF.readlines():
    sent, label = line.split(labelSeparator)
    label = label.rstrip()
    sents.append(sent)
    labels.append(label)

  expF.close()
  return sents, labels

def get_training_data():
  return get_experiment_data(trainFile)

def get_test_data():
  return get_experiment_data(testFile)

def prepare_training_data():
  import commands
  from BeautifulSoup import BeautifulSoup

  trainSamples = codecs.open(trainFile, 'w', encoding)
  testSamples  = codecs.open(testFile , 'w', encoding)

  files        = commands.getoutput('find ' + archiveLocation +
                                    ' -type f ')

  limit = 1
  for htmlf in files.rstrip().split('\n'):
    if limit == stopLimit: break
    limit +=1
    f = codecs.open(htmlf, 'r', encoding)
    text = ''
    for line in f.readlines():
      line = line.replace('\n', ' ')
      text += line
    f.close()
    soup = BeautifulSoup(text)
    tables = soup.findAll('table')
    #first table contains the steps
    trs = tables[0].findAll('tr')

    prev = None
    for tr in trs:
      tds = tr.findAll('td')
      if(len(tds) == 0): continue  #th row
      if prev == None:
        prev = tds[1].text #second column has text
        continue

      curr = tds[1].text

      tP = round(random.random(),2)
      nP = round(random.random(),2)

      if tP >= testP:
        if nP >= negativeP:
          sample = curr + blockSeparator \
                   + prev + labelSeparator + '-'
        else:
          sample = prev + blockSeparator \
                   + curr + labelSeparator + '+'

        testSamples.write(sample + '\n')
      else:
        if nP >= negativeP:
          sample = curr + blockSeparator \
                   + prev + labelSeparator + '-'
        else:
          sample = prev + blockSeparator \
                   + curr + labelSeparator + '+'

        trainSamples.write(sample + '\n')

      prev = curr

  testSamples.close()
  trainSamples.close()

def prepare_test_data():
  pass

def preprocess():
  prepare_training_data()
  prepare_test_data()

def run_classifier():
  print 'getting training data...'
  sents, labels = get_training_data()
  pprint(sents)
  pprint(labels)
  print len(labels)

  print 'training on the data...'
  ft_xtractor, clf = train(sents, labels)

  print 'getting test data...'
  test_sents, expected_labels = get_test_data()
  pprint(test_sents)
  pprint(expected_labels)
  print len(expected_labels)

  print 'using the model to predict...'
  pred_labels = test(test_sents, ft_xtractor, clf)
  correct = evaluate(pred_labels, expected_labels)

  print 'prediction results...'
  print str(correct) + ' correct out of ' + str(len(expected_labels)) + ' predictions'

def main():
  print 'Preprocessing...'
  preprocess()
  print 'Preparing classifier...'
  run_classifier()

if __name__ == '__main__':
  main()
