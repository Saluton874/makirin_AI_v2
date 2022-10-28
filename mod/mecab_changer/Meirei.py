import re
import jaconv
# 命令形。「命令ｅ」「命令ｒｏ」「命令ｙｏ」「命令ｉ」
class Meirei:
    def __init__(self):
        self.__re = re.compile(r'^命令(.+)$')
    # 「命令*」
    def get(self, row):
        return row[0] if self.__re.match(row[9]) else None
    # 「命令ｅ」
    def get_e(self, row):
        return row[0] if '命令ｅ' == row[9] else None
    # 「命令ｒｏ」
    def get_ro(self, row):
        return row[0] if '命令ｒｏ' == row[9] else None
    # 「命令ｙｏ」
    def get_yo(self, row):
        return row[0] if '命令ｙｏ' == row[9] else None
    # 「命令ｉ」
    def get_i(self, row):
        return row[0] if '命令ｉ' == row[9] else None

