################################################
#                                              #
#   author :	Jingxin Li <504914116@qq.com>  #
#   date	 :  Mar 25, 2013                   #
#                                              #
################################################
#! /usr/bin/python

from __future__ import division
from collections import defaultdict
tag_count = defaultdict(int)
word_tag_count = defaultdict(int)
train_words = set()
e = defaultdict(int)

def find_target_words(train_file):
	word_dict = dict()
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
			if word_dict[word] < 5:
				o_f.write('%s %s\n'%('_RARE_',tag))
			else:
				o_f.write('%s %s\n'%(word,tag))
		else:
			o_f.write('\n')
		l = f.readline()
	o_f.close()
	f.close()

# read in new counts file
# read tags counts
# read tag,word counts
# calculate emission probability
# output to file: tag word count

# build tag counts (tag,count)
# build word tag counts (word,tag,count)
def build_counts(counts_file):
	f 	= open(counts_file)
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			field	= line.split(" ")
			count   = field[0]
			kind	= field[1]
			if kind == 'WORDTAG':
				word = field[-1]
				tag  = field[-2]
				word_tag_count[word,tag] = count
				train_words.add(word)
			if kind == '1-GRAM':
				tag  = field[2]
				tag_count[tag] = count
		l = f.readline()
	f.close()

def em_prob(counts_file='gene.counts.replace',out_file='emission.out'):
	build_counts(counts_file)
	for word,tag in word_tag_count:
		e[word,tag] = int(word_tag_count[word,tag])/int(tag_count[tag])

def part1(dev_file ='gene.test',out_file='gene_test.p1.out'):
	f 	= open(dev_file)
	o_f = open(out_file,'w')
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			mx = 0
			for tag in ['O','I-GENE']:
				if line not in train_words:
					t_word = '_RARE_'
				else:
					t_word = line
				if (t_word,tag) not in e:
					continue
				else:
					#print t_word,line,tag,word_tag_count[t_word,tag],tag_count[tag],e[t_word,tag]
					if e[t_word,tag] > mx:
						mx = e[t_word,tag]
						mx_w = line
						mx_t = tag
			o_f.write(mx_w + " "+ mx_t + "\n")
		else: # empty line
			o_f.write('\n')

		l = f.readline()
	f.close()
	o_f.close()

def save_train_words(out_file='train.words'):
	o_f = open(out_file,'w')
	for w in train_words:
		o_f.write(w + ' ')
	o_f.close()

rewrite(train_file = 'gene.train', out_file = 'gene.out')
#em_prob()
#part1()
