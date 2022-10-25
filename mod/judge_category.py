#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' cat_and_point(text) … [カテゴリ名, ポイント] '''

import G
import sqlite3, MeCab
from operator import itemgetter # ソート用モジュール

dbpath = G.path+'dataset/db/単語分類表.db'

def cat_and_point(text):
    conn   = sqlite3.connect(dbpath)
    c      = conn.cursor()
    word_li= MeCab.Tagger(G.neologd+'-F%f[6],').parse(text).split(',')
    li     = []
    for i, word in enumerate(word_li):
        try:
            c.execute('SELECT label,score FROM categorize WHERE word=?', (word,))
        except: pass
        else:
            float_tuple = c.fetchone()
            if type(float_tuple) == tuple: li.append(float_tuple)
    conn.close()
    kind = []
    for tuples in li:
        kind.append([tuples[0].split('・')[0],tuples[1]])
    # ソートする
    kind.sort(key=itemgetter(0))
    # 同一カテゴリのものは合算する
    for i, item in enumerate(kind):
        if kind[i-1][0] == item[0]:
            kind[i][1] = kind[i-1][1]+item[1]
    # 最も高いカテゴリを選出する
    high_score = 0
    for item in kind:
        if high_score < item[1]:
            high_score = item[1]
            high_score_item = item
    if li:
        cat = high_score_item[0].split('・')
        cat.append(high_score_item[1])
        return cat
    return ['未分類',0]

if __name__ == "__main__": 
    print(cat_and_point(input('入力：')))