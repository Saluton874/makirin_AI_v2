#!/usr/bin/env python3
# -*- coding:utf-8 -*-

''' プルチック風感情中枢もどき '''

import time
from judge_kanjou import kanjou
timer = time.perf_counter()

class Plutchik:
	def __init__(self):
		self.plut = {'感情':'普通','心':{
			'安らぎ':0,
			'容認':0,
			'不安':0,
			'動揺':0,
			'感傷的':0,
			'倦怠': 0,
			'苛立ち':0,
			'関心':0
		}}

	def main(self,text):
		global timer
		for inp in kanjou(text):
		
			if inp in ['安らぎ','喜び','幸福感','穏やか','気持ちが良い']:
				# 安らぎ ++
				self.plut['心']['安らぎ'] += 2
				self.plut['心']['感傷的'] -= 2
			if inp in ['楽しさ', '感謝','祝う気持ち','好き','興奮']:
				# 安らぎ
				self.plut['心']['安らぎ'] += 1
				self.plut['心']['感傷的'] -= 1
			if inp in ['穏やか','誇らしい','尊敬・尊さ']:
				# 容認 ++
				self.plut['心']['容認'] += 2
				self.plut['心']['倦怠'] -= 2
			if inp in ['親しみ','祝う気持ち','好き']:
				# 容認
				self.plut['心']['容認'] += 1
				self.plut['心']['倦怠'] -= 1
			if inp in ['苦しさ','不安','恐怖','心配']:
				# 不安 ++
				self.plut['心']['不安'] += 2
				self.plut['心']['苛立ち'] -= 2
			if inp in ['焦り','恥ずかしい','きまずさ','あわれみ','ためらい','緊張']:
				# 不安
				self.plut['心']['不安'] += 1
				self.plut['心']['苛立ち'] -= 1
			if inp in ['驚き','恐れ（恐縮等の意味で）','失望']:
				# 動揺 ++
				self.plut['心']['動揺'] += 2
				self.plut['心']['関心'] -= 2
			if inp in ['あきれ','恥ずかしい','きまずさ','あわれみ','緊張','残念','困惑']:
				# 動揺
				self.plut['心']['動揺'] += 1
				self.plut['心']['関心'] -= 1
			if inp in ['寂しさ','悲しさ','失望','悩み','謝罪']:
				# 感傷的 ++
				self.plut['心']['感傷的'] += 2
				self.plut['心']['安らぎ'] -= 2	
			if inp in ['あきれ','切なさ','辛さ','残念','悔しさ','困惑','情けない']:
				# 感傷的
				self.plut['心']['感傷的'] += 1
				self.plut['心']['安らぎ'] -= 1	
			if inp in ['憎い','嫌悪','怠さ','悩み','謝罪']:
				# 倦怠 ++
				self.plut['心']['倦怠'] += 2
				self.plut['心']['容認'] -= 2		
			if inp in ['憂鬱','悔しさ','恨み','情けない']:
				# 倦怠
				self.plut['心']['倦怠'] += 1
				self.plut['心']['容認'] -= 1
			if inp in ['不満','怒り']:
				# 苛立ち ++
				self.plut['心']['苛立ち'] += 2
				self.plut['心']['不安'] -= 2	
			if inp in ['恨み','不快','妬み']:
				# 苛立ち
				self.plut['心']['苛立ち'] += 1
				self.plut['心']['不安'] -= 1
			if inp in ['願望','感動']:
				# 関心 ++
				self.plut['心']['関心'] += 2
				self.plut['心']['動揺'] -= 2	
			if inp in ['興奮','不快','妬み']:
				# 関心
				self.plut['心']['関心'] += 1
				self.plut['心']['動揺'] -= 1
	
		# 上限と下限の処理（±20まで）
		if abs(self.plut['心']['安らぎ']) > 20:
			self.plut['心']['安らぎ'] = -20 if self.plut['心']['安らぎ'] < 0 else 20
		if abs(self.plut['心']['容認']) > 20:
			self.plut['心']['容認'] = -20 if self.plut['心']['容認'] < 0 else 20
		if abs(self.plut['心']['不安']) > 20:
			self.plut['心']['不安'] = -20 if self.plut['心']['不安'] < 0 else 20
		if abs(self.plut['心']['動揺']) > 20:
			self.plut['心']['動揺'] = -20 if self.plut['心']['動揺'] < 0 else 20
		if abs(self.plut['心']['感傷的']) > 20:
			self.plut['心']['感傷的'] = -20 if self.plut['心']['感傷的'] < 0 else 20
		if abs(self.plut['心']['倦怠']) > 20:
			self.plut['心']['倦怠'] = -20 if self.plut['心']['倦怠'] < 0 else 20
		if abs(self.plut['心']['苛立ち']) > 20:
			self.plut['心']['苛立ち'] = -20 if self.plut['心']['苛立ち'] < 0 else 20
		if abs(self.plut['心']['関心']) > 20:
			self.plut['心']['関心'] = -20 if self.plut['心']['関心'] < 0 else 20
	
		# 値の高い順に並び替え
		a = sorted(self.plut['心'].items(), key=lambda i: i[1], reverse=True)
	
		# 1番目に高い数値が5以上である場合、感情名を代入
		if a[0][1] > 5:
			self.plut['感情'] = a[0][0]
		else:
			self.plut['感情'] = '普通'
		# 1、2番目に高い数値が5以上であり、2つの値の差が2以下である場合、「中間」の感情名を代入 ←なんか処理おかしい
		# ただし隣り合わない感情は処理しない
		if a[0][1] > 5 and a[1][1] > 5 and a[0][1] - a[1][1] <= 5:
			_ = [a[0][0],a[1][0]] # 順番関係なし
			if '安らぎ' in _ and '容認' in _:
				self.plut['感情'] = '愛'
			if '容認' in _ and '不安' in _:
				self.plut['感情'] = '服従'
			if '不安' in _ and '動揺' in _:
				self.plut['感情'] = '畏れ'
			if '動揺' in _ and '感傷的' in _:
				self.plut['感情'] = '失望'
			if '感傷的' in _ and '倦怠' in _:
				self.plut['感情'] = '自責の念'
			if '倦怠' in _ and '苛立ち' in _:
				self.plut['感情'] = '軽蔑'
			if '苛立ち' in _ and '関心' in _:
				self.plut['感情'] = '好戦的'
			if '関心' in _ and '安らぎ' in _:
				self.plut['感情'] = '楽観'

		def timer_point(now_point, point):
			# 今のポイントが0ならば0
			if now_point == 0: return 0
			# ポイントの変動が0を越す場合は現在のポイント分変動＝0になるように
			if abs(now_point) - point < 0:
				return abs(now_point) if now_point < 0 else -abs(now_point)
			# ポイントの変動
			return point if now_point < 0 else -point
		
		# 120秒経過ごとに値を0に近づける
		keika = time.perf_counter() - timer
		if keika > 120:
			point = round(keika / 120) # 経過回数
			self.plut['心']['安らぎ'] += timer_point(self.plut['心']['安らぎ'], point)
			self.plut['心']['容認'] += timer_point(self.plut['心']['容認'], point)
			self.plut['心']['不安'] += timer_point(self.plut['心']['不安'], point)
			self.plut['心']['動揺'] += timer_point(self.plut['心']['動揺'], point)
			self.plut['心']['感傷的'] += timer_point(self.plut['心']['感傷的'], point)
			self.plut['心']['倦怠'] += timer_point(self.plut['心']['倦怠'], point)
			self.plut['心']['苛立ち'] += timer_point(self.plut['心']['苛立ち'], point)
			self.plut['心']['関心'] += timer_point(self.plut['心']['関心'], point)
			timer = time.perf_counter() # 経過時間を再セット
	
		return self.plut

if __name__ == "__main__":
	plutchik = Plutchik()
	while True:
		inp = input('入力：')
		print(plutchik.main(inp))