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

#POSTags looked up from http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

###Parameters
testP           = 0.9 #rand >= testP for test sample
negativeP       = 0.45 # rand >= negativeP for negative sample
negativePTest   = 0.50 # rand >= negativeP for negative sample
trainFile       = 'trainSamples.txt' #train samples generated and then used
testFile        = 'testSamples.txt'  # same for test samples
archiveLocation = '/Users/gt/CookScrap/VR/transitions-2-pretty-V'
encoding        = 'utf-8' #encoding per website
stopLimit       = 612 #dev parameter - to check the sanity of the whole process
blockSeparator  = ' #BLOCK# ' #separator for 2 blocks
labelSeparator  = ' #LABEL# ' # separates the block and the label
#Both stanford pos tagger and default nlkt pos tagger are using same labels for pos taggin
filterList = ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', #Verb forms
                 'RB', 'RBR', 'RBS', 'WRB', #ADV
				'PRP', 'PRP$', 'WP', 'WP$',	#pronouns
              ] #Pos tags to be filtered

###

def train(sents, labels):
  ft_extractor,X = get_features(sents)
  #cache for the kernel in MB
  # clf            = svm.SVC(kernel='rbf', cache_size=1024, C=1000.0)
  # clf = svm.SVC(C=0.10000000000000001, cache_size=200, class_weight=None, coef0=0.0,
  #               degree=3, gamma=0.01, kernel='rbf', max_iter=-1, probability=False,
  #               random_state=None, shrinking=True, tol=0.001, verbose=False
  # )

  #Tuned kernel for all words unigram, bigram
  # clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
  #               gamma=0.001, kernel='rbf', max_iter=-1, probability=False,
  #               random_state=None, shrinking=True, tol=0.001, verbose=False)
  clf = svm.SVC(C=0.01, cache_size=200, class_weight=None, coef0=0.0, degree=3,
  gamma=1.0000000000000001e-05, kernel='linear', max_iter=-1,
  probability=False, random_state=None, shrinking=True, tol=0.001,
  verbose=False)

  clf.fit(X,labels)
  return ft_extractor,clf

def getBestEstimator(X, labels):
  # from sklearn.preprocessing import Scaler
  import numpy as np
  from sklearn.grid_search import GridSearchCV
  from sklearn.cross_validation import StratifiedKFold

  # scaler = Scaler()
  # X = scaler.fit_transform(X)

  C_range = 10. ** np.arange(-2, 9)
  gamma_range = 10. ** np.arange(-5, 4)

  param_grid = dict(gamma=gamma_range, C=C_range)

  grid = GridSearchCV(svm.SVC(kernel='linear'), param_grid=param_grid, cv=StratifiedKFold(y=labels, k=5))

  grid.fit(X, labels)

  print("The best classifier is: ", grid.best_estimator_)


def test(sents, ft_extractor, clf):
  X = ft_extractor.transform(sents)
  y = clf.predict(X)
  return y

def evaluate(observed, expected):
  if len(observed) != len(expected):
    raise 'Number of observations != Number of experiments'

  ctr = 0
  tpr = 0
  fpr = 0

  for i in range(len(observed)):
    if observed[i] != expected[i] and observed[i] == '+':
      fpr += 1
    if observed[i] == expected[i]:
      if(observed[i] == '+'):
        tpr +=1
      ctr+=1

  tpr = tpr * 100.0
  fpr = fpr * 100.0
  tpr = tpr / (len([x for x in expected if x == '+']))
  fpr = fpr / (len([x for x in expected if x == '-']))
  print "TPR " + str(tpr)
  print "FPR " + str(fpr)
  print "Observed + " + str(len([x for x in observed if x == '+']))
  print "Observed - " + str(len([x for x in observed if x == '-']))
  return ctr

def nltk_filter(sent):
  b1, b2 = sent.split(blockSeparator)
  b2 = b2.rstrip()

  b1            = b1.lower()
  tokens        = word_tokenize(b1)
  pos_tags      = pos_tag(tokens)
  filtered_sent = ' '
  for token in tokens:
    filtered_sent += '1'+token + ' '
  # for pos_t in pos_tags:
  #   if pos_t[1] in filterList:
  #     #filtered_sent += stemmer.stem(pos_t[0]) + ' '
  #     filtered_sent += '1' + stemmer.stem(pos_t[0]) + ' '

#note: 1 concat stemmer(word) == stemmer(1 concat word)

  b2            = b2.lower()
  tokens        = word_tokenize(b2)
  pos_tags      = pos_tag(tokens)
  # filtered_sent = ' '
  # for pos_t in pos_tags:
  #   if pos_t[1] in filterList:
  #     #filtered_sent += stemmer.stem(pos_t[0]) + ' '
  #     filtered_sent += '2' + stemmer.stem(pos_t[0]) + ' '

  for token in tokens:
    filtered_sent += '2' + token + ' '

  return filtered_sent

def stanford_corenlp_filter(sent):
  from nltk.tag.stanford import POSTagger
  posTagger = POSTagger('/Users/gt/Downloads/'
                        'stanford-postagger-2013-06-20/models/'
                        'wsj-0-18-bidirectional-nodistsim.tagger',
                        '/Users/gt/Downloads/stanford-postagger-2013-06-20'
                        '/stanford-postagger-3.2.0.jar',encoding=encoding)

  b1, b2 = sent.split(blockSeparator)
  b2 = b2.rstrip()

  b1 = b1.lower()
  tokens = word_tokenize(b1)
  pos_tags = posTagger.tag(tokens)
  filtered_sent = ' '
  for pos_t in pos_tags:
    if pos_t[1] in filterList:
      # filtered_sent += stemmer.stem(pos_t[0]) + ' '
      filtered_sent += '1' + stemmer.stem(pos_t[0]) + ' '

      #note: 1 concat stemmer(word) == stemmer(1 concat word)

  b2 = b2.lower()
  tokens = word_tokenize(b2)
  pos_tags = posTagger.tag(tokens)
  filtered_sent = ' '
  for pos_t in pos_tags:
    if pos_t[1] in filterList:
      # filtered_sent += stemmer.stem(pos_t[0]) + ' '
      filtered_sent += '2' + stemmer.stem(pos_t[0]) + ' '

  return filtered_sent


def filter_text(sent):
  # return stanford_corenlp_filter(sent)
  return nltk_filter(sent)


def get_features(sents):
  vec = CountVectorizer(min_df=1, binary=True, tokenizer=word_tokenize,
                        preprocessor=filter_text, ngram_range=(1,2) )
  X   = vec.fit_transform(sents)
  #pprint(str(X))
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
        if nP >= negativePTest:
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
  # print 'getting training data...'
  sents, labels = get_training_data()
  # pprint(sents)
  # pprint(labels)
  print 'Training set size ' + str(len(labels))

  # print 'training on the data...'
  ft_xtractor, clf = train(sents, labels)

  print 'number of features: ' + str(len(ft_xtractor.get_feature_names()))

  # print 'getting test data...'
  test_sents, expected_labels = get_test_data()
  # pprint(test_sents)
  # pprint(expected_labels)
  print 'Testing set size ' + str(len(expected_labels))

  # print 'using the model to predict...'
  pred_labels = test(test_sents, ft_xtractor, clf)
  correct = evaluate(pred_labels, expected_labels)

  print 'prediction accuracy...'
  print str( (correct * 100.0) / len(expected_labels))

def findEstimator():
  sents, labels = get_training_data()
  ft_extractor, X = get_features(sents)
  getBestEstimator(X,labels)


def main():
  # print 'Preprocessing...'
  # preprocess() #fixed the data
  # print 'Running classifier...'
  run_classifier()
  # findEstimator()

if __name__ == '__main__':
  main()
  print '#############'
