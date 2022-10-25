#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://www.tdi.co.jp/miso/python-natural-language-processing

import G
import MeCab
import pandas as pd
import csv, os


def kanjou(inp):
	m = MeCab.Tagger(G.neologd+'-F%f[6],')
	df_data = (inp)
	td = []
	
	temp = m.parse(df_data).split(',')[:-1]
	td.append(temp)

	df = pd.read_csv(G.path+"dataset/D18-2018.7.24/D18-2018.7.24.csv")
	pn_df = pd.read_csv(G.path+"dataset/D18-2018.7.24/PositiveNegativeSymbol.csv")
	
	pnWord_dic=[]
	 
	 
	## 形態素解析対象のループ
	 
	for i in range (0,len(df),1):
		temp = []
		tempEmotion = []
		
		temp.append(m.parse(df['Word'][i]).split(',')[:-1])
		
		## 作業者シートのEmotionが複数の感情を持つデータ用にループ
		
		for j in range(0, len(df['Emotion'][i]),1):
	 
			
			## 作業者シートのEmotionが感情シートのSymbolに無い場合のエラー回避
			
			if (len(pn_df[pn_df.Symbol==df['Emotion'][i][j]])!=0):
				
				
				## 感情分類シートのEmotionとPosNeg抽出
				
				tempEmotion.append(pn_df[pn_df.Symbol==df['Emotion'][i][j]].values[0][0])
		
		
		temp.append(tempEmotion)
		
		## Emotionと形態素解析したWordを変数に代入
		pnWord_dic.append(temp)
	 
	pnWord_dic = pd.DataFrame(pnWord_dic, columns=['Word','Emotion'])
	
	
	temp = ['Word','Emotion']
	results = []
	results.append(temp)
	
	for j in range(0,len(td),1):
	
		temp = []
	
		Exp = []
		emotion = []
		
		## 日本語感情辞書をループ
		for i in range(0,len(pnWord_dic),1):
	
	
			## 日本語感情辞書の内容がTweetに含まれる場合
			if (set(pnWord_dic['Word'][i]).issubset(td[j])):
	
				## 感情を表現している言葉とその感情の抽出
				Exp.append(pnWord_dic['Word'][i])
				emotion.extend(pnWord_dic['Emotion'][i])
	
		## データレコードの生成
		temp.append(td)
		temp.append(emotion)
		
		results.append(temp)

	tt = pd.DataFrame(results, columns=[ 'Word','Emotion' ])
	
	## 176番目～177番目のデータが見やすいので、そこに表示を限定しています。
	
	return tt['Emotion'][1]

if __name__ == "__main__":
	inp = input('入力：')
	print(kanjou(inp))