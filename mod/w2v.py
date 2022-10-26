#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# http://ai-coordinator.jp/slackbot
# https://swdrsker.hatenablog.com/entry/2017/02/23/193137
# https://qiita.com/To_Murakami/items/cc225e7c9cd9c0ab641e
# https://kamo.hatenablog.jp/entry/2020/04/05/173810

''' Word2Vecで似たベクトルの単語を選出する '''

import G
from gensim.models import KeyedVectors

def similar(inp):
	kvs = KeyedVectors.load(G.path+'dataset/w2v_model/wiki.kv')
	# wiki.kv.vectors.npy も必要
	try:
		return kvs.most_similar([inp], [], 1)[0][0]
	except:
		return inp

if __name__ == '__main__':
	while True:
		inp = input('入力：')
		print(similar(inp))