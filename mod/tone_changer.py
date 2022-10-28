#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# https://upwrite.jp/grammar/
# https://m4fqr9ys6jbetjb.hatenablog.com/entry/2018/02/18/202533
# https://qiita.com/anmorenight/items/3be08333d85648faad43
# https://foolean.net/index.html@p=132.html
# https://ytyaru.hatenablog.com/entry/2021/11/19/000000
# https://dspace.jaist.ac.jp/dspace/bitstream/10119/17249/5/paper.pdf
# https://www.kokugobunpou.com/助動詞/助動詞活用表/#gsc.tab=0
# https://ytyaru.hatenablog.com/entry/2021/11/23/000000

''' 言い換え '''
import sys
sys.path.append("mecab_changer")

import G, MeCab, re, sys
import pykakasi # ローマ字変換
import mecab_changer.ConjugationConvertor as ConjugationConvertor

owakati = MeCab.Tagger(G.neologd+'-Owakati')
bunpou = MeCab.Tagger(G.neologd+'-F,%f[0]|%f[1]|%f[2]|%f[5]|%f[6] -E,')
c = ConjugationConvertor.ConjugationConvertor()

class Changer():
	
	def __init__(self):
		self.sentence = []

	def standard(self, text):
		'''
		なんかおかしい日本語を簡易的に標準化
		TODO: なるますとか防ぎたい
		'''
		temp1 = owakati.parse(text).split()
		temp2 = bunpou.parse(text).split(',') #['', '感動詞|||こんにちは', '名詞|固有名詞|一般|ご機嫌いかが', '']
		sets = list(zip(temp1,temp2[1:-1]))
	
		for i, _ in enumerate(sets):
			self.sentence.append(_[0]) # 元の文章
			m = _[1].split('|') # めかぶ
			try: # 一つ前のめかぶ
				m_b = temp2[1:-1][i-1].split('|')
			except:
				m_b = [''] * 5

			print(self.sentence[i], m)

			'''
			格助詞の修正
			'''
			if '格助詞' in m:
				try:
					hepburn = pykakasi.kakasi().convert(sets[i+1][1].split('|')[3])[-1]['hepburn']
				except:
					hepburn = ''
				print(hepburn)
				# ざっくり他動詞
				if re.search('asu|yasu|osu|eru|seru|su', hepburn):
					self.sentence[i] = 'が'
				# ざっくり自動詞
				elif re.search('eru|ru|iru|reru|aru|waru|mu|iu|au|ku', hepburn):
					self.sentence[i] = 'を'
				# わからないのはスルー
				else:
					pass
			
			'''
			です・ますの修正
			'''
			if '助動詞' in m:
				# ですチェック
				if self.sentence[i] in ['でしょ','でし','です']:
					if m_b[1] in ['形容動詞語幹'] or \
						m_b[0] in ['名詞'] or \
						m_b[2] in ['助動詞語幹'] or \
						self.sentence[i] in ['でしょ'] and m_b[0] in ['動詞'] or \
						self.sentence[i] in ['でしょ'] and m_b[0] in ['形容詞']:
							if self.sentence[i] in ['でしょ']: self.sentence[i-1] = m_b[4]
							print('OK')
					else:
						# ます化させてみる
						if self.sentence[i] in ['でしょ']: self.sentence[i] = 'ましょ'
						if self.sentence[i] in ['でし']: self.sentence[i] = 'まし'
						if self.sentence[i] in ['です']: self.sentence[i] = 'ます'

				# ますチェック
				if self.sentence[i] in ['ませ','ましょ','まし','ます','ますれ']:
					if m_b[3] in ['連用形']:
						print('OK')
					else:
						print(c.get(self.sentence[i-1])['連用形'])
						self.sentence[i-1] = c.get(self.sentence[i-1])['連用形'][0][:-1] # 連用形にする

		return self.sentence

if __name__ == '__main__':
	changer = Changer()
	print(changer.standard(input('入力：')))