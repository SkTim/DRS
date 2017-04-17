# lhy
# 2017.4

import re
import json

class KB:

    def __init__(self, route):
        self.text = open(route, 'r').read()
        self.in_list = self.text.split('\n')
        self.pattern = re.compile(r'\w+_\w+')
    
    def load_kb(self, route_kb):
        self.kb = json.load(route_kb)
        return self.kb
    
    def load_rela(self):
        rela = self.pattern.findall(self.text)
        self.rela_dict = {}
        for r in rela:
            self.rela_dict[r] = ''
    
    def index_line(self, line):
        line = line[2:]
        rela = self.pattern.search(line).group()
        movie, enti = line.split(' %s ' % rela)
        if rela == 'has_plot':
            enti = [enti]
        else:
            enti = enti.split(', ')
        return (movie.encode('utf-8'), rela, enti)
    
    def build_kb(self):
        self.kb = {}
        self.load_rela()
        for line in self.in_list:
            if line == '':
                continue
            movie, rela, enti = self.index_line(line)
            if movie not in self.kb:
                self.kb[movie] = self.rela_dict.copy()
            self.kb[movie][rela] = enti
        return self.kb
    
    def movie_name(self):
        movies = self.kb.keys()
        movie_dict = dict([(x, i) for (i, x) in enumerate(movies)])
        return movie_dict
    
    def save_kb(self, route_kb, route_movie):
        kb = self.build_kb()
        movies = self.movie_name()
        json.dump(kb, open(route_kb, 'wb'))
        json.dump(movies, open(route_movie, 'wb'))

if __name__ == '__main__':
    kb = KB('../data/movie_dialog_dataset/movie_kb.txt')
    kb.save_kb('../data/movie_kb_dict.json',
        '../data/movie_name_dict.json')