#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# https://onl.sc/eEbUfhj

''' 簡易要約 '''

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from operator import itemgetter
from text_normalize import normalize as nor

def youyaku(text, gyou = 4):
	#全ての行を結合
	document = text
	# 自動要約のオブジェクトを生成
	auto_abstractor = AutoAbstractor()
	# トークナイザー（単語分割）にMeCabを指定
	auto_abstractor.tokenizable_doc = MeCabTokenizer()
	# 文書の区切り文字を指定
	auto_abstractor.delimiter_list = ["。", "\n"]
	# キュメントの抽象化、フィルタリングを行うオブジェクトを生成
	abstractable_doc = TopNRankAbstractor()
	# 文書の要約を実行
	result_dict = auto_abstractor.summarize(document, abstractable_doc)
	
	# 文章とスコアを結びつけてタプル化
	tuples = []
	for i,x in enumerate(result_dict["scoring_data"]):
		tuples.append(tuple([result_dict["summarize_result"][i]]) + x)
	
	# スコアごとに順序入れ替え
	tuples.sort(key=itemgetter(0, 2), reverse=True)
	
	#要約結果の取り出し
	sentence = ''
	for i, x in enumerate(tuples):
		if i == gyou: break
		sentence += x[0]
	
	return nor(sentence)

if __name__ == "__main__":
	print(youyaku('人間がお互いにコミュニケーションを行うための自然発生的な言語である。「自然言語」に対置される語に「形式言語」「人工言語」がある。形式言語との対比では、その構文や意味が明確に揺るぎなく定められ利用者に厳格な規則の遵守を強いる（ことが多い）形式言語に対し、話者集団の社会的文脈に沿った曖昧な規則が存在していると考えられるものが自然言語である。自然言語には、規則が曖昧であるがゆえに、話者による規則の解釈の自由度が残されており、話者が直面した状況に応じて規則の解釈を変化させることで、状況を共有する他の話者とのコミュニケーションを継続する事が可能となっている。',2))