# lhy
# 2017.4

import re
import json
import cPickle

def str_rep(text, rep):
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text

def add_relation(text, d_words):
    pattern = re.compile(r'\w+_\w+')
    match = set(pattern.findall(text))
    # print(len(match))
    n = len(d_words)
    for r in match:
        d_words[r] = str(n)
        n += 1
    d_rela = {}
    for r in match:
        d_rela[r] = d_words[r]
    return d_words, d_rela

class Prep:
    
    def __init__(self, route):
        self.dict_r = route + 'dictionary.txt'
        self.enti_r = route + 'entities.txt'
        self.kb_r = route + 'movie_kb.txt'
        self.qa_r = route + 'task1_qa/'
        self.recs_r = route + 'task2_resc/'
        self.pattern = pattern = re.compile(r'\w+_\w+')
    
    def load_dict(self):
        in_list = open(self.dict_r, 'r').readlines()
        words = [x.strip('\n') for x in in_list]
        d_words = [(x, str(i)) for i, x in enumerate(words)]
        self.d_words = dict(d_words)
        return self.d_words
    
    def load_enti(self):
        in_list = open(self.enti_r, 'r').readlines()
        entities = [x.strip('\n') for x in in_list]
        d_enti = [(x, str(i)) for i, x in enumerate(entities)]
        self.d_enti = dict(d_enti)
        self.d_words_all = self.d_words.copy()
        n_w = len(self.d_words)
        for enti in self.d_enti:
            self.d_words_all[enti] = str(n_w)
            n_w += 1
        d_enti_dict = [(x, self.d_words_all[x]) for x in entities]
        self.d_enti_dict = dict(d_enti_dict)
        return self.d_enti, self.d_enti_dict
    
    def index_line(self, line):
        if line == '':
            return ''
        if 'plot' in line:
            return ''
        # print(len(line))
        line = line[2:]
        relation = self.pattern.search(line).group()
        # print(relation)
        enti, ans = line.split(' %s ' % relation)
        ans_enti = ans.strip('\n').split(', ')
        try:
            enti_rela_index = [str(self.d_enti[enti]), str(self.d_rela[relation])]
            ans_index = [self.d_enti[x] for x in ans_enti]
        except:
            return ''
        return ' '.join(enti_rela_index + ans_index) + '\n'
    
    def load_kb(self):
        text = open(self.kb_r, 'r').read()
        in_list = text.split('\n')
        self.d_enti_rela, self.d_rela = add_relation(text, self.d_enti)
        # print(in_list[0])
        # text = self.index_line(in_list[0])
        index_list = [self.index_line(line) for line in in_list]
        text = ''.join(index_list)
        # text = str_rep(text, self.d_enti_dict)
        # text = str_rep(text, {',': ' ,', '...': '', '.': ' .', ':': ' :', ';': ' ;'})
        # text = str_rep(text, self.d_words)
        # text = text.replace('entity', '')
        return text
    
    def load_qa(self):
        pass
        text = open(self.qa_r, 'r').read()
        text = text.replace('\n', '')
        in_list = text.split('1 ')[1:]
    
    def load_recs(self):
        pass
    
    def save_dict(self, config):
        if config == 'json':
            pkg = json
        if config == 'cPickle':
            pkg = cPickle
        json.dump({'d_words' : self.d_words,
            'd_enti' : self.d_enti,
            'd_enti_rela' : self.d_enti_rela},
            open('data/enti_dict.%s' % config, 'wb'))
        print('Dictionary saved')