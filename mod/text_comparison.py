#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# https://d-cubed-lab.com/python-word2vec

''' 文章の比較（似た文脈かどうか） '''

import G, MeCab
import numpy as np
from gensim.models import KeyedVectors

# 似た文脈かどうか
def comparison(text1,text2):
	tagger = MeCab.Tagger(G.neologd+'-F%f[6],')
	model  = KeyedVectors.load(G.path+'dataset/w2v_model/wiki.kv')
	# ベクトル平均を計算
	def get_vector(text):
		text = tagger.parse(text)
		sum_vec = np.zeros(50)
		word_count = 0
		node = tagger.parseToNode(text)
		while node:
			fields = node.feature.split(',')
			if fields[0] == '名詞': # 動詞はエラーしまくった
				sum_vec += model[node.surface]
				word_count += 1
			node = node.next
		return sum_vec / word_count

	text1 = get_vector(text1)
	text2 = get_vector(text2)
	sim = np.dot(text1, text2) / (np.linalg.norm(text1) * np.linalg.norm(text2))
	return sim

if __name__ == "__main__": 
    print(comparison('犬と猫を飼った','ネコは寝転んだ'))