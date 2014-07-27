import nltk
import re
import json

nltk.download('maxent_ne_chunker')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('punkt')
nltk.download('words')

def do_ner(text):
	print text
	rl = []
	np = []
	ne = []
        for sentence in nltk.sent_tokenize(text): #re.sub(r'[^\x00-\x7F]+',' ', text)):

            sentence_tok = nltk.word_tokenize(sentence)
            sentence_tok = nltk.pos_tag(sentence_tok)


	    grammar = r"""
  NP: {<PP\$>?<JJ|JJR|JJS>*<NN|NNP|NNS|NNPS>+}   # chunk adjectives and noun
""" #      {<NNP>+}                # chunk sequences of proper nouns
#"""        
            cp = nltk.RegexpParser(grammar)

	    ret = dict()
            ret['sentence'] = sentence
            ret['npr'] = cp.parse(sentence_tok)
            ret['ner'] = nltk.ne_chunk(sentence_tok, binary=True)
	    ret['noun_phrases_tree'] = filter(lambda x: x.node == 'NP', ret['npr'].subtrees())
	    ret['named_entities_tree'] = filter(lambda x: x.node == 'NE', ret['ner'].subtrees())
	    np += [" ".join(w[0] for w in t.leaves()) for t in ret['noun_phrases_tree']]
	    ne += [" ".join(w[0] for w in t.leaves()) for t in ret['named_entities_tree']]
	    rl.append(ret)
	ne_sort = list(set(ne))
	np_sort = list(set(np))
	ne_sort.sort(key=len, reverse=True)
	np_sort.sort(key=len, reverse=True)
	np_filter = filter(lambda x: len(x) >= 15, np_sort)
	best_guess = []
	best_guess += ne_sort[:10]
	if len(ne_sort) == 0:
		best_guess += np_filter[:10]
	else:
		best_guess += np_filter[:5]
	if len(best_guess) == 0:
		best_guess += np_sort
	return json.dumps({'noun_phrases': np, 'named_entities': ne, 'best_guess':best_guess}, sort_keys=True, indent=4, separators=(',',': '))
