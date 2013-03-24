################################################
#                                              #
#   author :	Jingxin Li <504914116@qq.com>  #
#   date	 :  Mar 25, 2013                   #
#                                              #
################################################


#! /usr/bin/python
import unigram_tagger
import re
from collections import defaultdict

censored_list 	= defaultdict(str)
word_dict		= dict()

# (word,type)
def classify_train_data(word):
	if word_dict[word] < 5: # rare
		if is_numeric(word):
			return '_NUMERIC_'
		elif is_all_caps(word):
			return '_ALLCAPS_'
		elif is_last_cap(word):
			return '_LASTCAP_'
		else:
			return '_RARE_'
	else:# >5 words
		return word

def is_numeric(word):
	if re.search(r'\d+',word):
		return True
	else:
		return False

def is_all_caps(word):
	if re.search(r'\b[A-Z]+\b',word):
		return True
	else:
		return False

def is_last_cap(word):
	if re.search(r'[A-Z]$',word):
		return True
	else:
		return False


def find_target_words(train_file):
	f = open(train_file)
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			field = line.split(" ")
			word  = field[0]
			if word in word_dict:
				word_dict[word] += 1
			else:
				word_dict[word] = 1
		l = f.readline()
	f.close()
	return word_dict

def rewrite(train_file, out_file):
	word_dict = find_target_words(train_file)
	o_f = open(out_file,'w')
	f = open(train_file)
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			field = line.split(" ")
			word  = field[0]
			tag   = field[1]
			classified_word  = classify_train_data(word)
			o_f.write('%s %s\n'%(classified_word,tag))
		else:
			o_f.write('\n')
		l = f.readline()
	o_f.close()
	f.close()



rewrite(train_file='gene.train',out_file='gene.out.classified')



