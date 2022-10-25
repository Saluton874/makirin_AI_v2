#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' 簡易否定確認 '''

import G, MeCab

def hitei_bool(text):
	temp1 = MeCab.Tagger(G.neologd+'-Owakati').parse(text).split()
	temp2 = MeCab.Tagger(G.neologd+'-F,%f[1] , -U,%m , -E,').parse(text).split(',')
	temp3 = MeCab.Tagger(G.neologd+'-F,%f[0] , -U,%m , -E,').parse(text).split(',')
	for i, _ in enumerate(zip(temp1,temp2[1:-1],temp3[1:-1])):
		if _[1] in ['接尾辞','接頭詞','形容詞','名詞'] and _[0] in ['非','不','無','未','反','異','無い','無し']:
			return True
		if _[2] in ['助動詞'] and _[0] in ['ない','ぬ','ん']:
			if not temp1[i-1] in ['なく']: return True # わからなくない対策
	return False

if __name__ == "__main__": 
    print(hitei_bool(input('入力：')))