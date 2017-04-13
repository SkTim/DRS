# lhy
# 2017.4

from preprocessing import prep

p = prep.Prep('data/movie_dialog_dataset/')
d = p.load_dict()
d1, d2 = p.load_enti()
# kb = p.load_kb()
# qa = p.load_qa('task1_qa_test.txt')
recs = p.load_recs('task2_recs_test.txt')
# print(recs)
# open('data/movie_kb_index.txt', 'w').write(kb)
# open('data/movie_qa_index.txt', 'w').write(qa)
open('data/movie_recs_index.txt', 'w').write(recs)
# p.save_dict('json')