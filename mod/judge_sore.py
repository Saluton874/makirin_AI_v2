#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# https://qiita.com/ayuchiy/items/c3f314889154c4efa71e

''' なんちゃってソレ探し '''

import G
import re, MeCab, CaboCha
from text_normalize import normalize as nor
from judge_category import cat_and_point

owakati = MeCab.Tagger(G.neologd+'-Owakati')
bunpou = MeCab.Tagger(G.neologd+'-F,%f[1] , -U,%m , -E,')
bunpou2 = MeCab.Tagger(G.neologd+'-F,%f[0]%f[1]%f[2], -U,%m , -E,')
c = CaboCha.Parser(G.neologd)

def eq(self, a, b):
    an = Analyzer()
    c = an.analyze(a)
    self.assertEqual(c, b)

def check_sore(p_text1, p_text2):

	# 形態素を結合しつつ[{c:文節, to:係り先id}]の形に変換する
	def make_chunks(tree):
		chunks = []
		toChunkId = -1
		for i in range(0, tree.size()):
			token = tree.token(i)
			text = token.surface if token.chunk else (text + token.surface) 
			toChunkId = token.chunk.link if token.chunk else toChunkId
			# 文末かchunk内の最後の要素のタイミングで出力
			if i == tree.size() - 1 or tree.token(i+1).chunk:
			   chunks.append({'c': text, 'to': toChunkId})
		return chunks
	
	chunks =  make_chunks(c.parse(nor(p_text2+' '+p_text1)))

	# 係り元→係り先の形式で出力する
	sentence = {}

	for chunk in chunks:
		if chunk['to'] >= 0:
			temp1 = owakati.parse(chunk['c']).split()
			temp2 = bunpou.parse(chunk['c']).split(',')
			for _ in zip(temp1,temp2[1:-1]):
				sentence |= {chunk['c']:chunks[chunk['to']]['c']}	

	result = []

	hito = False
	mono = False
	basho = False
	hougaku = False

	for v in sentence.keys():
		temp1 = owakati.parse(v).split()
		temp2 = bunpou2.parse(v).split(',')
		jyogai= owakati.parse(p_text2).split() # 自身の発言には「それ」がないと仮定
		for i, _ in enumerate(temp1):
			# 「これ、ここ、こちら」は自分で提示しているので無変換
			# 「どれ、どこ、どちら」は相手が提示しているので無変換
			if _ in ['その人','その子','そいつ','誰']:
				hito = _
			elif _ in ['それ','あれ','その']:
				mono = _
			elif _ in ['そこ','あそこ','どこ']:
				basho = _
			elif _ in ['そちら','あちら']:
				hougaku = _

		# 複数ある場合は……どうしようかな
		for _ in zip(temp1, temp2[1:-1]):
			if _[0] in jyogai: continue
			
			cat = cat_and_point(_[0])
			
			if hito and _[1] in ['名詞固有名詞人名']:
				result.append(_[0])
			elif mono and _[1] in ['名詞一般','名詞固有名詞一般']:
				result.append(_[0])
			elif basho and _[1] in ['名詞固有名詞地域'] or re.search('宿泊|施設',cat[0]) or re.search('(?!(出|入|退|登|開|閉|下))(校|学|市|所|区|場|地|海|家|園|廷|州|国)$',_[0][-1]):
				result.append(_[0])
			elif hougaku and _[1] in ['名詞固有名詞地域'] or re.search('宿泊|施設',cat[0]) or re.search('(?!(出|入|退|登|開|閉|下))(校|学|市|所|区|場|地|海|家|園|廷|州|国)$',_[0][-1]):
				result.append(_[0])

	if len(result) == 0:
		if hito: return hito
		elif mono: return mono
		elif basho: return basho
		elif hougaku: return hougaku
		else: return False

	return result[0] # とりあえず一番最初に出てきた単語にしておく

if __name__ == '__main__':
	print(check_sore('ラーメンは美味しい','それは食べ物かな'))