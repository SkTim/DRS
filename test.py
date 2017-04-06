# lhy
# 2017.4

from preprocessing import prep

p = prep.Prep('data/movie_dialog_dataset/')
d = p.load_dict()
d1, d2 = p.load_enti()
text = p.load_kb()
open('data/movie_kb_index.txt', 'w').write(text)
p.save_dict('json')