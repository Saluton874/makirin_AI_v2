#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# https://qiita.com/hnishi/items/0d32a778e375a99aff13

''' ネガポジ判定モジュールのテスト '''

from asari.api import Sonar
sonar = Sonar()

if __name__ == "__main__":
	inp = input('入力：')
	print(sonar.ping(text=inp))