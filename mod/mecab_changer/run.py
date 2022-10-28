#!/usr/bin/env python3
# coding: utf8
import ConjugationConvertor

c = ConjugationConvertor.ConjugationConvertor()
bases = ['走る','押す','愛する','見る','食べる','来る','悲しい','ござる']
for base in bases:
    d = c.get(base)
    for conj in d.keys():
        print('===== {} {} ====='.format(base, conj))
        for word in d[conj]:
            print(word)

"""
定まる,772,772,6852,動詞,自立,*,*,五段・ラ行,基本形,定まる,サダマル,サダマル

0: 語(word)
1,2,3:
4: 品詞(word_class)
5: 単語種別(word_type)
6,7:
8: 活用種別(conj_type) 
9: 活用形種別(conj)
10: 語の基本形(word_base)
11,12: 読み？発音？
"""
