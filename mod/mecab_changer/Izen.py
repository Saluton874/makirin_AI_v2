import re
import jaconv
# 已然形。仮定形ともいう。「仮定形」「仮定縮約１」など
class Izen:
    def __init__(self):
        self.__re_min = re.compile(r'^仮定縮約(.+)$')
    # 「ば」
    def get_ba(self, row):
        if '仮定形' == row[9]: return row[0] + 'ば'
#        if '未然形' == row[9] or '未然特殊' == row[9]: return row[0] + 'ない'
        else: return None
    # 「ども」
    def get_domo(self, row):
        if '仮定形' == row[9]: return row[0] + 'ども'
        else: return None
    # 「たら」
    def get_tara(self, row):
        if '仮定形' == row[9]: return row[0] + 'たら'
        else: return None
    # 「れば」
    def get_reba(self, row):
        if '仮定形' == row[9] and not ('一段' in row[8] or '二段' in row[8]): return row[0] + 'れば'
        else: return None
    # 「る」
    def get_ru(self, row):
        if '仮定形' == row[9]: return row[0] + 'る'
        else: return None
    # 「れる」
    def get_reru(self, row):
        if '仮定形' == row[9] and not ('一段' in row[8] or '二段' in row[8]): return row[0] + 'れる'
        else: return None
    # 「仮定縮約１」など
    def get_min(self, row):
        m = self.__re_min.match(row[9])
        if m: return row[0]
        else: return None

