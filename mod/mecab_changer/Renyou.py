import re
import jaconv
# 連用形。動詞の前に来る
class Renyou:
    def __init__(self):
        self.__re_conj_conn = re.compile(r'^連用(.+)接続$')
    # 「方」
    def get_howto(self, row):
        if '連用形' == row[9]: return row[0] + '方'
#        if '未然形' == row[9] or '未然特殊' == row[9]: return row[0] + 'ない'
        else: return None
    # 「様」
    def get_state(self, row):
        if '連用形' == row[9]: return row[0] + '様'
        else: return None
    # 「始める」
    def get_start(self, row):
        if '連用形' == row[9]: return row[0] + '始める'
        else: return None
    # 「終わる」
    def get_end(self, row):
        if '連用形' == row[9]: return row[0] + '終わる'
        else: return None
    # 「連用タ接続」など
    def get_conn(self, row):
        m = self.__re_conj_conn.match(row[9])
        if m: return row[0] + jaconv.kata2hira(m.group(1))
        else: return None

