# lhy
# 2017.4

from preprocessing import prep

# '''
p = prep.Prep('data/movie_dialog_dataset/')
d = p.load_dict()
d1, d2 = p.load_enti()
kb = p.load_kb()
# qa = p.load_qa('task1_qa_test.txt')
recs_train = p.load_recs_name('task2_recs_train.txt')
recs_dev = p.load_recs_name('task2_recs_dev.txt')
recs_test = p.load_recs_name('task2_recs_test.txt')
# print(recs)
open('data/movie_kb_index.txt', 'w').write(kb)
# open('data/movie_qa_index.txt', 'w').write(qa)
open('data/recs_name_idx_train.txt', 'w').write(recs_train)
open('data/recs_name_idx_dev.txt', 'w').write(recs_dev)
open('data/recs_name_idx_test.txt', 'w').write(recs_test)
# p.save_dict('json')
# '''

prep.movie2dict('data/movie_dialog_dataset/dictionary.txt',
    'data/movie_name_dict.json',
    'data/recs_name_idx_train.txt',
    'data/recs_idx_train.txt')

prep.movie2dict('data/movie_dialog_dataset/dictionary.txt',
    'data/movie_name_dict.json',
    'data/recs_name_idx_dev.txt',
    'data/recs_idx_dev.txt')

prep.movie2dict('data/movie_dialog_dataset/dictionary.txt',
    'data/movie_name_dict.json',
    'data/recs_name_idx_test.txt',
    'data/recs_idx_test.txt')