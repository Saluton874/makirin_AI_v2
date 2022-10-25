#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# https://www.anlp.jp/proceedings/annual_meeting/2019/pdf_dir/P8-15.pdf
# https://qiita.com/ayuchiy/items/c3f314889154c4efa71e
# https://www.maytry.net/use-cabocha-with-python/

''' なんちゃって暴言感知 '''

import G, MeCab, re, CaboCha
import numpy as np
from text_normalize import normalize as nor
from gensim.models import KeyedVectors

with open(G.path+'dataset/暴言.txt','r') as f:
	bougen = f.read().replace('\n', '')

owakati = MeCab.Tagger(G.neologd+'-Owakati')
bunpou = MeCab.Tagger(G.neologd+'-F,%f[0]%f[1] , -U,%m , -E,')
c = CaboCha.Parser(G.neologd)

def check_bougen(p_text):
	tree=  c.parse(nor(p_text))
	
	# 罵倒と一致する部分をリスト化
	bougen_match = re.findall(bougen, p_text)
	bougen_match = bougen_match[0] if bougen_match else []

	# 形態素を結合しつつ[{c:文節, to:係り先id}]の形に変換する
	chunks = []
	toChunkId = -1
	for i in range(0, tree.size()):
		token = tree.token(i)
		text = token.surface if token.chunk else (text + token.surface) 
		toChunkId = token.chunk.link if token.chunk else toChunkId
		# 文末かchunk内の最後の要素のタイミングで出力
		if i == tree.size() - 1 or tree.token(i+1).chunk:
		   chunks.append({'c': text, 'to': toChunkId})
	
	# 係り元→係り先の形式で出力する
	sentence = []
	for chunk in chunks:
		if chunk['to'] >= 0:
			temp1 = owakati.parse(chunk['c']).split()
			temp2 = bunpou.parse(chunk['c']).split(',')
			for _ in zip(temp1,temp2[1:-1]):
				for b in bougen_match:
					if re.search(b, _[0]) and _[1] in ['名詞固有名詞','名詞一般'] and not _[1] in ['名詞接尾'] or _[0] == _[1] and not chunk['c'] in sentence:
						sentence.append(_[0]) # 何に対して暴言を吐いたのか

	return {
		'bool' : True if len(bougen_match) > 0 else False, # 暴言が含まれるか
		'target': list(set(sentence)) # 暴言の矛先
	}

if __name__ == '__main__':
	print(check_bougen(input('入力：')))