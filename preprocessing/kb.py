# lhy
# 2017.4

class KB_prep:
    
    def __init__(self, route):
        self.dict_r = route + 'dictionary.txt'
        self.enti_r = route + 'entities.txt'
        self.kb_r = route + 'movie_kb.txt'
        self.qa_r = route + 'task1_qa/'
        self.recs_r = route + 'task2_resc/'
    
    def load_dict(self):
        in_list = open(self.dict_r, 'r').readlines()
        words = [x.strip('\n') for x in in_list]
        d_words = [(x, str(i)) for i, x in enumerate(words)]
        self.d_words = dict(d_words)
        return self.d_words
    
    def load_enti(self):
        in_list = open(self.enti_r, 'r').readlines()
        entities = [x.strip('\n') for x in in_list]
        d_enti = [(x, self.d_words[x]) for x in entities]
        self.d_enti = dict(d_enti)
        return d_enti
    
    def load_kb(self):
        pass
    
    def load_qa(self):
        pass
    
    def load_recs(self):
        pass