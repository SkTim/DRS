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
        self.recs_r = route + 'task2_recs/'
        self.pattern = re.compile(r'\w+_\w+')
    
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
        # self.d_words_all = self.d_words.copy()
        # n_w = len(self.d_words)
        # for enti in self.d_enti:
        #     self.d_words_all[enti] = 'entity%s' % str(n_w)
        #     n_w += 1
        d_enti_dict = [(x.lower(), self.d_words[x.lower()]) for x in entities]
        self.d_enti_dict = dict(d_enti_dict)
        return self.d_enti, self.d_enti_dict
    
    def index_line_kb(self, line):
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
    
    def index_line_qa(self, line):
        if line == '':
            return ''
        line = line[2:]#.replace(',', '')
        ques, ans = line.strip('\n').split('?\t')
        q_words = ques.lower().split(' ')
        q_cache = []
        i = 0
        search_range = range(10)
        search_range.reverse()
        while i < len(q_words):
            word = q_words[i]
            s = 0
            for j in search_range:
                if i + j >= len(q_words):
                    continue
                query = ' '.join(q_words[i : i + j + 1]).strip(',')
                # if 'Jane?' in line:
                #     print(query)
                if query in self.d_enti_dict:
                    # print(query)
                    s = 1
                    i = i + j
                    break
            i += 1
            if s == 0:
                q_cache.append(self.d_words[word.replace(',', '')])
            else:
                q_cache.append(self.d_enti_dict[query])
        ques = ' '.join(q_cache)
        ans_enti = ans.split(', ')
        try:
            ans_idx = ' '.join([self.d_enti[x] for x in ans_enti])
        except:
            return ''
        text = '%s ? %s\n' % (ques, ans_idx)
        return text
    
    def index_line_recs(self, line, movies):
        # print(line)
        line = line[2:].strip('\n')
        query, recs = line.split('?\t')
        q_words = query.split(' ')
        # query_idx = [self.d_enti[x] for x in query_enti]
        # text = '%s %s' % (' '.join(query_idx), self.d_enti[recs])
        search_range = range(6)
        search_range.reverse()
        i = 0
        query_idx = []
        while i < len(q_words):
            for j in search_range:
                if i + j >= len(q_words):
                    continue
                query = ' '.join(q_words[i : i + j + 1]).strip(',')
                if query in movies:
                    query_idx.append(str(movies[query.decode('utf-8')]))
                    i = i + j
                    break
            i += 1
        return '%s %s\n' % (' '.join(query_idx), str(movies[recs.decode('utf-8')]))

    def load_kb(self):
        text = open(self.kb_r, 'r').read()
        in_list = text.split('\n')
        self.d_enti_rela, self.d_rela = add_relation(text, self.d_enti)
        index_list = [self.index_line_kb(line) for line in in_list]
        text = ''.join(index_list)
        return text
    
    def load_qa(self, data):
        in_list = open(self.qa_r + data, 'r').readlines()
        # text = self.index_line_qa(in_list[0])
        text = ''.join([self.index_line_qa(line) for line in in_list])
        return text
    
    def load_recs(self, data):
        movies = json.load(open('data/movie_name_dict.json', 'rb'))
        in_list = open(self.recs_r + data, 'r').readlines()
        text = ''.join([self.index_line_recs(line, movies) for line in in_list])
        return text
    
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