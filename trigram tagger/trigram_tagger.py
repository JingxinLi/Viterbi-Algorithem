################################################
#                                              #
#   author :	Jingxin Li <504914116@qq.com>  #
#   date	 :  Mar 24, 2013                   #
#                                              #
################################################


#! /usr/bin/python
from __future__ import division
from collections import defaultdict

unigram_count	= defaultdict(int)
bigram_count	= defaultdict(int)
trigram_count	= defaultdict(int)
word_tag_count  = defaultdict(int)
training_words	= set()
tags			= set()
start_tag		= '*'
stop_tag		= 'STOP'
rare_word		= '_RARE_'

# reads in count file
# stores bigram and trigram counts 
# in global bigram_count and trigram_count
# called by trans_prob_iterator()
def ngram_reader(in_file):
	
	f = open(in_file)
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			field	= line.split(" ")
			count 	= int(field[0])
			gram 	= field[1]
			if  gram == 'WORDTAG':
				word = field[-1]
				tag  = field[-2]
				word_tag_count[word,tag] = count
				training_words.add(word)
			elif gram == '1-GRAM': # unigrams
				unigram_count[field[2]] = count
				tags.add(field[2])
			elif gram == '2-GRAM': # bigrams
				bigram_count[tuple(field[2:])] = count			
			elif gram == '3-GRAM': # trigrams
				trigram_count[tuple(field[2:])] = count
		else: # empty line
			contine # ignore
		l = f.readline()
	f.close()

# returns an iterator with format (word)
# if it is an empty line, yield (None)
def file_iterator(in_file):
	f = open(in_file)
	l = f.readline()
	while l:
		line = l.strip()
		if line: # non-empty line
			yield (line)
		else: # empty line
			yield(None) 
		l = f.readline()
	f.close()

# calls file_iterator
# returns a sentence iterator
def sentence_iterator(file_itr):
	sentence = []
	for l in file_itr:
		if l == (None):
			# end of a sentence
			if sentence: # yield non-empty sentence
				yield(sentence)
				sentence = []
		else:
			sentence.append(l)
	if sentence: # in case, the file ends without empty line
		yield(sentence)

# save PA1 part2 results to file
def save_to_file(path,sentence,out_file):
	f = open(out_file,'a+')
	sentence_tag = zip(sentence,path)
	for pair in sentence_tag:
		word = pair[0]
		tag = pair[1]         
		f.write(word+' '+tag+'\n')
	f.write('\n')
	f.close()

def get_e(v,word):
	return float(word_tag_count[word,v] / unigram_count[v])

def get_q(w,u,v):
	return float(trigram_count[w,u,v]/bigram_count[w,u])

class HmmTagger:
	
	# choose right tag set for w,u,v
	# according to the position of the word
	def choose_tags(self,k,tags,start_tag,sent_num):
		if k == 1: # v in tags; w/u = *
			self.w_tags,self.u_tags = start_tag,start_tag
		elif k == 2: # v,u in tags; w  = *
			self.u_tags = tags
		elif k >2: # k>2, v,u,w in tags
			self.w_tags = tags

	def tagger(self,test_file,out_file):
		pi 	= defaultdict(float)
		for sent in sentence_iterator((file_iterator(test_file))):
			sent_num = sum(1 for _ in sent)
			self.v_tags = tags
			bp = {}

			# initial step
			pi[(0,start_tag,start_tag)] = 1
			bp[start_tag,start_tag] = [tag for tag in tags]

			# 1 to n steps
			for k in range(1,sent_num+1): # include the last word
				self.choose_tags(k,tags,start_tag,sent_num)
				u_tags,w_tags,v_tags = self.u_tags, self.w_tags, self.v_tags
				word = sent[k-1]# always use sent[k-1]
				temp_bp = {}
				if word not in training_words: # replace rare words
					word = rare_word
				for u in u_tags:
					for v in v_tags:
						pi[k,u,v],prev_w	= max((pi[k-1,w,u] * get_q(w,u,v) * get_e(v,word),w) for w in w_tags)
						temp_bp[u,v] 		= bp[prev_w,u] + [v]
				bp = temp_bp

			# last step
			mx = 0
			for v in v_tags:
				for u in u_tags:
					if pi[len(sent),u,v] * get_q(u,v,stop_tag) > mx:
						mx = pi[len(sent),u,v] * get_q(u,v,stop_tag)
						mx_u = u
						mx_v = v
			path = bp[mx_u,mx_v]

            # remove two * at the beginning and STOP at the end
			path.pop(0)
			path.pop(0)
			save_to_file(path,sent,out_file)


ngram_reader("gene.counts.revised")
hmm = HmmTagger()
hmm.tagger(test_file= 'gene.dev',out_file = 'gene_dev.p2.out')
#hmm.tagger(test_file= 'gene.test',out_file = 'gene_test.p2.out')