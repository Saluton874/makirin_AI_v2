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
		self.sentence_type = '不明' # どういう意図があるか

	def change_katsuyo(self, word, mode):
		try:
			if mode == '未然形':
				return c.get(word)['未然形'][0][:-2]
			if mode == '形容詞未然形':
				return c.get(word)['未然形'][1][:-1]
			if mode == '連用形':
				return c.get(word)['連用形'][0][:-1]
			if mode == '基本形':
				return ''.join(bunpou.parse(word).split(',')[1:-1]).split('|')[5]
		except:
			return word
	
	def reset_m(self):
		text = ''.join(self.sentence)
		temp2 = bunpou.parse(text).split(',')
		m = [''] * 3
		m[0] = ''.join(temp2[1:-1][-1]).split('|') # めかぶ
		try:
			m[1] = ''.join(temp2[1:-1][-2]).split('|')
		except:
			m[1] = [''] * 6
		try:
			m[2] = ''.join(temp2[1:-1][-3]).split('|')
		except:
			m[2] = [''] * 6
		return m

	def standard(self, text):
		'''
		なんかおかしい日本語を簡易的に修正
		完成後チェッカーだけ分ける
		'''
		self.sentence = []
		text = ''.join(self.sentence) if len(self.sentence) else text
		temp1 = owakati.parse(text).split()
		temp2 = bunpou.parse(text).split(',')
		sets = list(zip(temp1,temp2[1:-1]))
	
		for i, _ in enumerate(sets):
			self.sentence.append(_[0]) # 元の文章
			m = [''] * 3
			
			m[0] = _[1].split('|') # めかぶ
			try:
				m[1] = temp2[1:-1][i-1].split('|')
			except:
				m[1] = [''] * 6
			try:
				m[2] = temp2[1:-1][i-2].split('|')
			except:
				m[2] = [''] * 6

			print(self.sentence[i], m[0])

			'''
			格助詞の修正
			
			if '格助詞' in m[0]:
				# TODO:にがおかしい
				try:
					hepburn = pykakasi.kakasi().convert(sets[i+1][1].split('|')[3])[-1]['hepburn']
				except:
					hepburn = ''
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
			'''
			来る（カ変）の対策
			後から修正
			'''
			'''
			if '助動詞' in m:
				if re.search(r'カ変',m_b[3]) or re.search(r'来ら|来る|来れる|来意',m_b[5]):
					if re.search(r'サ変|ナイ',m[3]) or m[5] in ['さし'] or m[5] in ['ら'] or '助動詞' in m and not '不変化型' in m[3]:
						self.sentence[i-1] = '来' #未然形・連用形
					if self.sentence[i] in ['ら']:
						self.sentence[i] = ''
					if re.search(r'一段',m[3]):
						self.sentence[i-1] = '来さ'
			'''

			'''
			せるの修正
			'''
			if '動詞' in m[0]:
				if self.sentence[i] in ['せ','せる','せれ','せろ','せよ','させ','させる','させれ','させろ','させよ']:
					if m[1] in ['動詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '未然形')
				# せるチェック
				if self.sentence[i] in ['せ','せる','せれ','せろ','せよ']:
					m = self.reset_m()
					if m[1] in ['動詞']:
						if re.search(r'五段|サ変',m[1][3]):
							print('「せる」OK')
							self.sentence_type = '使役'
						else:
							# させる化させてみる
							if self.sentence[i] in ['せ']: self.sentence[i] = 'させ'
							if self.sentence[i] in ['せる']: self.sentence[i] = 'させる'
							if self.sentence[i] in ['せれ']: self.sentence[i] = 'させれ'
							if self.sentence[i] in ['せろ']: self.sentence[i] = 'させろ'
							if self.sentence[i] in ['せよ']: self.sentence[i] = 'させよ'
					elif not m[1][3] in ['一段'] and not self.sentence[i-1] in ['さ']:
						self.sentence[i] = 'さ'+self.sentence[i]
				# させるチェック（「来るさせる」とかは放置）
				if self.sentence[i] in ['させ','させる','させれ','させろ','させよ']:
					m = self.reset_m()
					if m[1][3] in ['五段・サ行']:
						self.sentence[i-1] = self.sentence[i-1][:-1]
					if m[1][3] in ['一段'] or re.search(r'来|こ',m[1][0]):
						print('「させる」OK')
						self.sentence_type = '使役'

			'''
			れるの修正
			'''
			if '動詞' in m[0]:
				if self.sentence[i] in ['れ','れる','れれ','れろ','れよ','られ','られる','られれ','られろ','られよ']:
					if m[1][0] in ['動詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '未然形')

				# れるチェック
				if self.sentence[i] in ['れ','れる','れれ','れろ','れよ'] and m[1][0]:
					m = self.reset_m()
					if m[1][0] in ['動詞']:
						if re.search(r'五段|サ変',m[1][3]):
							print('「れる」OK')
							self.sentence_type = '自発・尊敬'
						elif not m[1][3] in ['一段'] and not self.sentence[i-1] in ['さ']:
							self.sentence[i] = 'さ'+self.sentence[i]
						else:
							# られる化させてみる
							if self.sentence[i] in ['れ']: self.sentence[i] = 'られ'
							if self.sentence[i] in ['れる']: self.sentence[i] = 'られる'
							if self.sentence[i] in ['れれ']: self.sentence[i] = 'られれ'
							if self.sentence[i] in ['れろ']: self.sentence[i] = 'られろ'
							if self.sentence[i] in ['れよ']: self.sentence[i] = 'られよ'
				# られるチェック
				if self.sentence[i] in ['られ','られる','られれ','られろ','られよ'] and m[1][0]:
					m = self.reset_m()
					if m[1][5] in ['する']:
						self.sentence[i-1] = 'させ'
					if self.sentence[i-1] in ['れ']:
						self.sentence[i] = 'る'
					elif not m[1][3] in ['一段'] and not self.sentence[i-1] in ['させ']:
						self.sentence[i] = 'させ'+self.sentence[i]
					elif m[1][3] in ['一段'] or re.search(r'来|こ',m[1][0]):
						print('「られる」OK')
						self.sentence_type = '受け身・可能'

			'''
			ないの修正
			'''
			if m[1][0] in ['動詞','助動詞']: # 動詞と助動詞「ませ」の後に付く
				if self.sentence[i] in ['なかろ','なかっ','なく','ない','なけれ','ず','ぬ','ん','ね']:
					if m[1][0] in ['動詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '未然形')
				# ないチェック
				if '特殊・ナイ' in m and '未然形' in m[1][4]:
					m = self.reset_m()
					print('ないOK')
					self.sentence_type = '否定'
				# ぬんチェック
				if self.sentence[i] in ['ぬ','ん']:
					m = self.reset_m()
					if self.sentence[i-1] in ['ます','まし','ますれ','ましょ']:
						self.sentence[i-1] = 'ませ'
					self.sentence[i] = 'ん'
					print('ぬんOK')
					self.sentence_type = '否定'

			'''
			う・ようの修正
			'''
			if '不変化型' in m[0] and not m[0][5] in ['ぬ','ん'] or '助動詞語幹' in m[0]: # ようは助動詞語幹らしい
				if self.sentence[i] in ['う']:
					if m[1][0] in ['動詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '未然形')
					if m[1][0] in ['形容詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '形容詞未然形')

				if m[1][4] in ['未然ウ接続']:
					# うチェック
					if re.search(r'五段',m[1][3]) or re.search(r'形容動詞',m[1][1]):
						m = self.reset_m()
						if m[0][5] in ['よう']: self.sentence[i] = 'う'
						print('うOK')
						self.sentence_type = '推量'
					else:
						m = self.reset_m()
						if self.sentence[i-1] in ['されよ','れよ']:
							self.sentence[i-1] = 'れよ'
							try:
								if self.sentence[i-2] == 'さ':
									self.sentence[i-1] = 'せよ'
							except:
								pass
						print('ようOK')
						self.sentence_type = '意志'

				if m[1][0] in ['助動詞']:
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
				if m[0][5] == 'よう':
					if self.sentence[i-1] in ['せる','せれ','せろ','せよ']:
						self.sentence[i-1] = 'せ'
					if self.sentence[i-1] in ['させられる','させる','させれ','させろ','させよ']:
						self.sentence[i-1] = 'させ'
					if self.sentence[i-1] in ['れる','れれ','れろ','れよ']:
						self.sentence[i-1] = 'れ'
					if self.sentence[i-1] in ['られる','られれ','られろ','られよ']:
						self.sentence[i-1] = 'られ'

			'''
			たい・たがるの修正
			'''
			if m[0][3] in ['特殊・タイ'] or m[1][4] in ['ガル接続']:
				m = self.reset_m()
				if m[1][0] in ['動詞']:
					self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')
				# たいチェック
				if m[0][3] in ['特殊・タイ'] and '動詞' in m[1]:
					if self.sentence[i-1] in ['せる','せ','せれ','せろ','せよ']:
						self.sentence[i-1] = 'せ'
					print('たいOK')
					self.sentence_type = '希望'

				# たがるチェック
				if m[1][4] in ['ガル接続'] and self.sentence[i] in ['がる','がら','がっ','がり','がれ']:
					print('たがるOK')
					self.sentence_type = '希望'
			
			# ガル接続じゃないけど「がる」が来る場合
			elif self.sentence[i] in ['がる','がら','がっ','がり','がれ']:
				m = self.reset_m()
				if m[1][0] in ['動詞']:
					self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')
				self.sentence[i] = 'た'+self.sentence[i]

			'''
			た・だの修正
			幅広すぎてカバーできそうもない
			'''
			if m[0][3] in ['特殊・タ','特殊・ダ']:
				ta_flag = False # ○○なら対策
				m = self.reset_m()
				if m[0][4] in ['未然形','仮定形'] or m[0][4] in ['連用形'] and self.sentence[i] == 'で':
					ta_flag = True
					self.sentence[i-1] = m[1][5]
				elif m[1][0] in ['動詞']:
					self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')

				if m[1][0] in ['動詞'] or m[1][4] in ['連用タ接続'] or \
					not self.sentence[i-1] in ['ぬ','ん','う','まい']:
					if m[1][0] in ['助動詞'] or m[1][0] in ['動詞']:
						if self.sentence[i-1] in ['せる','せり','せれ','せろ','せよ']:
							self.sentence[i-1] = 'せ' if not ta_flag else 'せる' # 思わせるなら
						if self.sentence[i-1] in ['させる','さし','させれ','させろ','させよ']:
							self.sentence[i-1] = 'させ' if not ta_flag else 'させる' # 着させるなら
						if self.sentence[i-1] in ['れ','れる','れれ','れろ','れよ']:
							self.sentence[i-1] = 'れ' if not ta_flag else 'れる' #言われるなら
						if self.sentence[i-1] in ['させられる','られる','られれ','られろ','られよ']:
							self.sentence[i-1] = 'られ' if not ta_flag else 'られる' # 混ぜられるなら
						if self.sentence[i-1] in ['ない','なかろ','なく','なけれ']:
							self.sentence[i-1] = 'なかっ' if not ta_flag else 'ない' # 起きないなら
						if self.sentence[i-1] in ['たい','たかろ','たく','たけれ']:
							self.sentence[i-1] = 'たかっ' if not ta_flag else 'たい' # 働きたいなら
						if m[2][4] in ['ガル接続'] and self.sentence[i-1] in ['がる','がら','がり','がれ']:
							self.sentence[i-1] = 'がっ' if not ta_flag else 'がる' # 会わせたがるなら
						if self.sentence[i-1] in ['らしい','らしく','らしけれ']:
							self.sentence[i-1] = 'らしかっ' if not ta_flag else 'らしい' # 遊ぶらしいなら
						if self.sentence[i-1] in ['ます','ませ','ましょ','ますれ','ませまし']:
							self.sentence[i-1] = 'まし' if not ta_flag else 'ます' # 言いますなら
						if self.sentence[i-1] in ['だ','だろ','で','な','なら']:
							self.sentence[i-1] = 'だっ' if not ta_flag else 'た' # 嫌だったなら
						if self.sentence[i-1] in ['です','でしょ']:
							self.sentence[i-1] = 'でし' if not ta_flag else 'です' # 良いですなら？
					if m[1][3] in ['五段・ガ行','五段・ナ行','五段・バ行','五段・マ行']:
						if m[1][3] in ['五段・ガ行']:
							self.sentence[i-1] = self.sentence[i-1][:-1]+'い'
						else:
							self.sentence[i-1] = self.sentence[i-1][:-1]+'ん'
						self.sentence[i] = 'だ'
					if not '体言接続' in m[0]:
						self.sentence[i] = 'た' if not ta_flag else 'だ'
						if m[1][0] in ['名詞']: self.sentence[i] = 'だ'
					print('たOK')
					self.sentence_type = '過去・完了'

			'''
			そうだ・ようだの修正
			形態解析結果が特殊？で動作確認できていない
			'''
			if m[0][3] in ['特殊・ダ'] or self.sentence[i] in ['に','な']:
				m = self.reset_m()
				# そうだチェック
				if m[1][1] in ['助詞類接続'] and self.sentence[i-1] == 'そう':
					if m[2][0] in ['動詞']:
						self.sentence[i-2] = self.change_katsuyo(self.sentence[i-2], '連用形') 
					print('そうだOK')
					self.sentence_type = '様態'
				elif m[1][0] in ['動詞'] and self.sentence[i] in ['に','な']:
					self.sentence[i] = 'そう' + self.sentence[i]
				# ようだチェック
				if m[1][1] in ['助詞類接続'] and self.sentence[i-1] == 'よう':
					if m[2][0] in ['動詞','形容詞'] or \
						re.search(r'形容動詞',m[2][1]) or \
						m[2][0] in ['助詞'] and m[2][5] in ['の'] or \
						m[2][0] in ['連体詞'] and m[2][5] in ['この','その','あの','どの'] or \
						m[2][5] in ['せる','させる','れる','られる','ない','ぬ','ん','たい','たがる','た','だ']:
						print('ようだOK')
						self.sentence_type = '推定・たとえ'
						if self.sentence[i] == 'に':
							self.sentence_type = '例示'

			'''
			らしいの修正
			'''
			if m[0][0] in ['助動詞'] and m[0][3] in ['形容詞・イ段']:
				m = self.reset_m()
				if m[1][0] in ['動詞','形容詞','助動詞'] and not re.search(r'基本',m[1][4]):
					self.sentence[i-1] = m[1][5]
				if m[1][0] in ['動詞','形容詞','名詞'] or \
					m[1][1] in ['形容動詞語幹','副助詞'] or \
					m[1][1] in ['格助詞'] and m[1][5] in ['の','から'] or \
					m[1][5] in ['せる','される','れる','られる','ない','たい','たがる','た','だ']:
					print('らしいOK')
					self.sentence_type = '推定'

			'''
			です・ますの修正
			'''

			if m[0][3] in ['特殊・デス','特殊・マス'] and m[1][0]:
				# ますチェック
				if self.sentence[i] in ['ませ','ましょ','まし','ます','ますれ']:
					m = self.reset_m()
					if m[1][0] in ['動詞']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')
						print('「ます」OK')
						self.sentence_type = '丁寧'
					elif self.sentence[i-1] in ['せり','さし']:
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')
						if self.sentence[i-1] in ['せり']:
							self.sentence[i-1] = 'せ'
						if self.sentence[i-1] in ['さし']:
							self.sentence[i-1] = 'させ'
					else:
						# ます化させてみる
						if self.sentence[i] in ['ましょ']: self.sentence[i] = 'でしょ'
						if self.sentence[i] in ['まし']: self.sentence[i] = 'でし'
						if self.sentence[i] in ['ます']: self.sentence[i] = 'です'
				# ですチェック
				if self.sentence[i] in ['でしょ','でし','です']:
					m = self.reset_m()
					if m[1][1] in ['形容動詞語幹'] or \
						m[1][0] in ['名詞'] and not m[1][1] in ['非自立'] or \
						m[1][2] in ['助動詞語幹'] or \
						self.sentence[i] in ['です'] and m[1][0] in ['形容詞'] or \
						self.sentence[i] in ['でしょ'] and m[1][0] in ['動詞'] or \
						self.sentence[i] in ['でしょ'] and m[1][0] in ['形容詞']:
							if self.sentence[i] in ['でしょ']: self.sentence[i-1] = m[1][5]
							print('「です」OK')
							self.sentence_type = '断定'
					else:
						# ます化させてみる
						self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '連用形')
						if self.sentence[i] in ['でしょ']: self.sentence[i] = 'ましょ'
						if self.sentence[i] in ['でし']: self.sentence[i] = 'まし'
						if self.sentence[i] in ['です']: self.sentence[i] = 'ます'

						
			'''
			まいの修正
			'''
			if m[0][0] in ['助動詞'] and self.sentence[i] == 'まい' and m[1][0]:
				m = self.reset_m()
				print(m)
				if m[1][0] in ['動詞'] and re.search(r'五段',m[1][3]) or m[1][5] in ['ます']:
					self.sentence[i-1] = m[1][5]
					print('まいOK')
					self.sentence_type = '否定'
				elif m[1][5] in ['です']:
					self.sentence[i-1] = 'ます'
					print('まいOK')
					self.sentence_type = '否定'
				elif m[1][0] in ['動詞'] or \
					self.sentence[i-1] in ['せ','せる','せれ','せろ','せよ','させ','させる','させれ','させろ','させよ'] or \
					self.sentence[i-1] in ['れ','れる','れれ','れろ','れよ','られ','られる','られれ','られろ','られよ']:
					self.sentence[i-1] = self.change_katsuyo(self.sentence[i-1], '未然形')
					print('まいOK')
					self.sentence_type = '否定'

			'''
			その他の修正
			'''
			if m[1][0] and re.search(r'かっ',self.sentence[i-1]):
				m = self.reset_m()
				if m[1][4] == '連用タ接続':
					self.sentence[i] = 'たです'

		return self.sentence

	def check_auxiliary_verb(self):
		'''
		助動詞のチェック
		'''
		text = ''.join(self.sentence)
		temp1 = owakati.parse(text).split()
		temp2 = bunpou.parse(text).split(',')
		sets = list(zip(temp1,temp2[1:-1]))
		

if __name__ == '__main__':
	changer = Changer()
	'''
	with open(G.path+'dataset/日本語例文.txt','r') as f:
		for line in f:
			print('■ '+line)
			print(changer.standard(line))
			print('------------------------------')
	'''
	print(changer.standard(input('入力：')))