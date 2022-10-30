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
bunpou = MeCab.Tagger(G.neologd+'-F,%f[0]|%f[1]|%f[2]|%f[4]|%f[5]|%f[6] -E,')
c = ConjugationConvertor.ConjugationConvertor()

class Changer():
	
	def __init__(self):
		self.sentence = []

	def standard(self, text):
		'''
		なんかおかしい日本語を簡易的に標準化
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
				m_b = [''] * 6

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
			来る（カ変）の対策
			'''
			if re.search(r'カ変',m_b[3]) or re.search(r'来ら|来る|来れる|来意',m_b[5]):
				if re.search(r'サ変|ナイ',m[3]) or m[5] in ['さし'] or m[5] in ['ら'] or '助動詞' in m and not '不変化型' in m[3]:
					self.sentence[i-1] = '来' #未然形・連用形
				if self.sentence[i] in ['ら']:
					self.sentence[i] = ''
				if re.search(r'一段',m[3]):
					self.sentence[i-1] = '来さ'
					

			'''
			せるの修正
			'''
			if '動詞' in m:
				# 未然に未然形へ変更しておく
				if self.sentence[i] in ['せ','せる','せれ','せろ','せよ','させ','させる','させれ','させろ','させよ']:
					if m_b[0] in ['動詞'] and not re.search(r'未然',m_b[4]):
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['未然形'][0][:-2]
						except:
							pass
				# せるチェック
				if self.sentence[i] in ['せ','せる','せれ','せろ','せよ']:
					if m_b[0] in ['動詞'] and re.search(r'未然',m_b[4]):
						if re.search(r'五段|サ変',m_b[3]):
							print('「せる」OK')
						else:
							# させる化させてみる
							if self.sentence[i] in ['せ']: self.sentence[i] = 'させ'
							if self.sentence[i] in ['せる']: self.sentence[i] = 'させる'
							if self.sentence[i] in ['せれ']: self.sentence[i] = 'させれ'
							if self.sentence[i] in ['せろ']: self.sentence[i] = 'させろ'
							if self.sentence[i] in ['せよ']: self.sentence[i] = 'させよ'
					elif not m_b[3] in ['一段'] and not self.sentence[i-1] in ['さ']:
						self.sentence[i] = 'さ'+self.sentence[i]
				# させるチェック（「来るさせる」とかは放置）
				if self.sentence[i] in ['させ','させる','させれ','させろ','させよ']:
					if m_b[3] in ['一段'] or re.search(r'来|こ',m_b[0]):
						print('「させる」OK')

			'''
			れるの修正
			'''
			if '動詞' in m:
				# 未然に未然形へ変更しておく
				if self.sentence[i] in ['れ','れる','れれ','れろ','れよ','られ','られる','られれ','られろ','られよ']:
					if m_b[0] in ['動詞'] and not re.search(r'未然',m_b[4]):
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['未然形'][0][:-2]
						except:
							pass
				# れるチェック
				if self.sentence[i] in ['れ','れる','れれ','れろ','れよ']:
					if m_b[0] in ['動詞'] and re.search(r'未然',m_b[4]):
						if re.search(r'五段|サ変',m_b[3]):
							print('「れる」OK')
						else:
							# られる化させてみる
							if self.sentence[i] in ['れ']: self.sentence[i] = 'られ'
							if self.sentence[i] in ['れる']: self.sentence[i] = 'られる'
							if self.sentence[i] in ['れれ']: self.sentence[i] = 'られれ'
							if self.sentence[i] in ['れろ']: self.sentence[i] = 'られろ'
							if self.sentence[i] in ['れよ']: self.sentence[i] = 'られよ'
					elif not m_b[3] in ['一段'] and not self.sentence[i-1] in ['さ']:
						self.sentence[i] = 'さ'+self.sentence[i]
				# られるチェック
				if self.sentence[i] in ['られ','られる','られれ','られろ','られよ']:
					if not m_b[3] in ['一段'] and not self.sentence[i-1] in ['させ']:
						self.sentence[i] = 'させ'+self.sentence[i]
					if m_b[3] in ['一段'] or re.search(r'来|こ',m_b[0]):
						print('「られる」OK')

			'''
			ないの修正
			'''
			if '動詞' in m_b: # 「ない」は形容詞型と特殊型があるので、手前が動詞であることを条件とする
				# 未然に未然形へ変更しておく
				if self.sentence[i] in ['なかろ','なかっ','なく','ない','なけれ','ず','ぬ','ん','ね']:
					if m_b[0] in ['動詞'] and not re.search(r'未然',m_b[4]):
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['未然形'][0][:-2]
						except:
							pass
				# ぬんチェック
				if self.sentence[i] in ['ぬ','ん']:
					self.sentence[i] = 'ん'
					if not 'ませ' in m_b:
						self.sentence[i] = 'ません'

			'''
			う・ようの修正
			'''
			if '不変化型' in m or '助動詞語幹' in m: # (よ)うは存在しないっぽい？
				# 未然に未然形へ変更しておく
				if self.sentence[i] in ['う']:
					if m_b[0] in ['動詞'] and not re.search(r'未然',m_b[4]):
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['未然形'][0][:-2]
						except:
							pass
					if m_b[0] in ['形容詞'] and not re.search(r'未然',m_b[4]):
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['未然形'][1][:-1]
						except:
							pass
				if m_b[4] in '未然ウ接続':
					if self.sentence[i-1] in ['されよ','れよ']:
						self.sentence[i-1] = 'れよ'
						try:
							if self.sentence[i-2] == 'さ':
								self.sentence[i-1] = 'せよ'
						except:
							pass
					print('ようOK')
				else:
					if re.search(r'五段',m_b[3]) or re.search(r'形容動詞',m_b[1]):
						print('うOK')
				
				if m_b[0] in ['助動詞']:
					if self.sentence[i-1] in ['ない','なかっ','なく','なけれ']:
						self.sentence[i-1] = 'なかろ'
					if self.sentence[i-1] in ['たい','たかっ','たく','たけれ']:
						self.sentence[i-1] = 'たかろ'
					if self.sentence[i-1] in ['だ','だっ','で','な','なら']:
						self.sentence[i-1] = 'だろ'
					if self.sentence[i-1] in ['た','たら','だら']:
						self.sentence[i-1] = 'たろ'
					if self.sentence[i-1] in ['ようだ','ようだっ','ようで','ように','ような','ようなら']:
						self.sentence[i-1] = 'ようだろ'
					if self.sentence[i-1] in ['そうだ','そうだっ','そうで','そうに','そうな','そうなら']:
						self.sentence[i-1] = 'そうだろ'
					if self.sentence[i-1] in ['ます','まし','ますれ','ませ']:
						self.sentence[i-1] = 'ましょ'
					if self.sentence[i-1] in ['です','でし']:
						self.sentence[i-1] = 'でしょ'
				if m[5] == 'よう':
					if self.sentence[i-1] in ['せる','せ','せれ','せろ','せよ']:
						self.sentence[i-1] = 'せ'
					if self.sentence[i-1] in ['させる','させ','させれ','させろ','させよ']:
						self.sentence[i-1] = 'させ'
					if self.sentence[i-1] in ['れる','れ','れれ','れろ','れよ']:
						self.sentence[i-1] = 'れ'
					if self.sentence[i-1] in ['られる','られ','られれ','られろ','られよ']:
						self.sentence[i-1] = 'られ'

			'''
			です・ますの修正
			'''
			if '助動詞' in m:
				# ですチェック
				if self.sentence[i] in ['でしょ','でし','です']:
					if m_b[1] in ['形容動詞語幹'] or \
						m_b[0] in ['名詞'] and not m_b[1] in ['非自立'] or \
						m_b[2] in ['助動詞語幹'] or \
						self.sentence[i] in ['です'] and m_b[0] in ['形容詞'] or \
						self.sentence[i] in ['でしょ'] and m_b[0] in ['動詞'] or \
						self.sentence[i] in ['でしょ'] and m_b[0] in ['形容詞']:
							if self.sentence[i] in ['でしょ']: self.sentence[i-1] = m_b[5]
							print('「です」OK')
					else:
						# ます化させてみる
						if self.sentence[i] in ['でしょ']: self.sentence[i] = 'ましょ'
						if self.sentence[i] in ['でし']: self.sentence[i] = 'まし'
						if self.sentence[i] in ['です']: self.sentence[i] = 'ます'

				# ますチェック
				if self.sentence[i] in ['ませ','ましょ','まし','ます','ますれ']:
					if m_b[3] in ['連用形']:
						print('「ます」OK')
					else:
						try:
							self.sentence[i-1] = c.get(self.sentence[i-1])['連用形'][0][:-1] # 連用形にする
							if self.sentence[i-1] in ['せり']:
								self.sentence[i-1] = 'せ'
						except:
							pass
					try:
						if self.sentence[i-1] in ['さし']:
							self.sentence[i-1] = 'させ'
					except:
						pass

		return self.sentence

if __name__ == '__main__':
	changer = Changer()
	print(changer.standard(input('入力：')))