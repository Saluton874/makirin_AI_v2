#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' negaposi(text) … ポイントを取得できます '''

import G
import sqlite3, MeCab

dbpath = G.path+'dataset/db/単語感情極性対応表.db'

def negaposi(text):
    conn   = sqlite3.connect(dbpath)
    c      = conn.cursor()
    word_li= MeCab.Tagger(G.neologd+'-F%f[6],').parse(text).split(',')
    li     = []
    for i, word in enumerate(word_li):
        try:
            c.execute('SELECT 数値 FROM 単語感情極性対応表 WHERE 単語=?', (word,))
        except: pass
        else:
            float_tuple = c.fetchone()
            if type(float_tuple) == tuple: li.append(float_tuple[0])
    conn.close()
    return sum(li)

if __name__ == "__main__":
	inp = input('入力：')
	print(negaposi(inp))