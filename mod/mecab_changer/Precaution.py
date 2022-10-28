#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
# MeCabのCSVから用言データを抽出する
class Precaution:
    def __init__(self, dic_dir: str=''):
        if dic_dir is None or (isinstance(dic_dir, str) and 0 == len(dic_dir)):
            self.__dic_dir = os.getcwd()
        else: self.__dic_dir = dic_dir
    def __csv_files(self):
        # 用言（動詞、形容詞、助動詞）
        return ('Verb.utf8.csv', 'Adj.utf8.csv', 'Auxil.utf8.csv')
    # 指定した用言（基本形）がもつ活用形名の一覧を返す。
    def get_conjugations(self, word):
        return self.__get_csv_rows(
            lambda row: word == row[10],
            lambda row: row[9])
    # 指定した用言（基本形）に一致するレコードの活用形を返す
    def get_conj_word(self, word, conj):
        return self.__get_csv_row(
            lambda row: word == row[10] and conj == row[9],
            lambda row: row[0])
    # 指定した用言（基本形）に一致するレコードの活用形名と活用形を返す
    def get_conj_words(self, word):
        return self.__get_csv_rows(
            lambda row: word == row[10],
            lambda row: {'conj': row[9], 'word': row[0]})
    # 指定した用言（基本形）に一致するレコードを丸ごと返す
    def get(self, word):
        return self.__get_csv_rows(
            lambda row: word == row[10],
            lambda row: row)
    def __get_csv_rows(self, lcond, lres):
        res = []
        for filename in self.__csv_files():
            reader = csv.reader(open(os.path.join(self.__dic_dir, filename), "r", encoding="utf-8"))
            for row in reader:
                if lcond(row): res.append(lres(row))
            if 0 < len(res): return res
        return res
    def __get_csv_row(self, lcond, lres):
        for filename in self.__csv_files():
            reader = csv.reader(open(os.path.join(self.__dic_dir, filename), "r", encoding="utf-8"))
            for row in reader:
                if lcond(row): return lres(row)
        return None

