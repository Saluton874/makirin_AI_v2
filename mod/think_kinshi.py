#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# http://monoroch.net/kinshi/

''' 禁止用語処理 '''

# 参考資料内で禁止とされている単語に限る

import G
import pandas as pd

def iikae(text):
	df = pd.read_csv(filepath_or_buffer=G.path+'dataset/kinshi.csv')
	a = df['用語'] == text
	for i, catch in enumerate(a):
		if catch == True:
			if type(df['言い換え'][i]) == float:
				return '禁止用語'
			else:
				return df['言い換え'][i].split('\n')[0]
	else:
		return text

if __name__ == '__main__':
	print(iikae('按摩'))