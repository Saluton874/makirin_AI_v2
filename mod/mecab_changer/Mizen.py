import re
import jaconv
class Mizen:
    def __init__(self):
        self.__re_conj_conn = re.compile(r'^未然(.+)接続$')
    # 「ない」
    def get_not(self, row):
        if '未然形' == row[9] or '未然特殊' == row[9]: return row[0] + 'ない'
        else: return None
    # 「ず」
    def get_not_old(self, row):
        if '未然形' == row[9]: return row[0] + 'ず'
        else: return None
    # 「未然ウ接続」など
    def get_conn(self, row):
        m = self.__re_conj_conn.match(row[9])
        if m: return row[0] + jaconv.kata2hira(m.group(1))
        else: return None
    # 「ん」
    def get_not_special(self, row):
        if '未然特殊' == row[9]: return row[0] + 'ねぇ'
        else: return None
    # 「れる／られる」受け身・可能・自発・尊敬
    def get_reru(self, row):
        if '未然形' == row[9]:
            if '五段' in row[8] or 'サ変' in row[8]: return row[0] + 'れる'
            if '一段' in row[8] or 'カ変' in row[8]: return row[0] + 'られる'
            raise Exception('れる/られるパターン外: {}, {}'.format(row[8], row))
        else: return None

