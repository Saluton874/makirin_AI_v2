#!/usr/bin/env python3
# coding: utf8
import Precaution
import Meirei
import Izen
import Renyou
import Mizen
class ConjugationConvertor:
    def __init__(self):
        self.__precation = Precaution.Precaution()
        self.__mizen = Mizen.Mizen()
        self.__renyou= Renyou.Renyou()
        self.__izen = Izen.Izen()
        self.__meirei = Meirei.Meirei()
    # 指定した用言（基本形）の未然、連用、已然、命令形を返す
    def get(self, word):
        mizen  = []
        renyou = []
        izen   = []
        meirei = []
        for row in self.__precation.get(word):
            mizen.extend(self.__get_mizen(row))
            renyou.extend(self.__get_renyou(row))
            izen.extend(self.__get_izen(row))
            meirei.extend(self.__get_meirei(row))
        mizen  = self.__remove_none(mizen)
        renyou = self.__remove_none(renyou)
        izen   = self.__remove_none(izen)
        meirei = self.__remove_none(meirei)
        return {
            '未然形': mizen,
            '連用形': renyou,
            '已然形': izen,
            '命令形': meirei,
        }
    def __get_mizen(self, row):
        return [self.__mizen.get_not(row),
                self.__mizen.get_not_old(row),
                self.__mizen.get_conn(row),
                self.__mizen.get_not_special(row),
                self.__mizen.get_reru(row)]
    def __get_renyou(self, row):
        return [self.__renyou.get_howto(row),
                self.__renyou.get_state(row),
                self.__renyou.get_start(row),
                self.__renyou.get_end(row),
                self.__renyou.get_conn(row)]
    def __get_izen(self, row):
        return [self.__izen.get_ba(row),
                self.__izen.get_domo(row),
                self.__izen.get_tara(row),
                self.__izen.get_reba(row),
                self.__izen.get_ru(row),
                self.__izen.get_reru(row),
                self.__izen.get_min(row)]
    def __get_meirei(self, row):
        return [self.__meirei.get(row)]
#    return (meirei.get(row),
#            meirei.get_e(row),
#            meirei.get_ro(row),
#            meirei.get_yo(row),
#            meirei.get_i(row))
    def __remove_none(self, arr): return [x for x in arr if x is not None]

"""
定まる,772,772,6852,動詞,自立,*,*,五段・ラ行,基本形,定まる,サダマル,サダマル

0: 語(word)
1,2,3:
4: 品詞(word_class)
5: 単語種別(word_type)
6,7:
8: 活用種別(conj_type) 
9: 活用形種別(conj)
10: 語の基本形(word_base)
11,12: 読み？発音？
"""
