# datasetの中身について

自分メモです。

## dbフォルダ

SQlite3のデータベースを格納しています。

### 単語分類表

[単語感情極性対応表](http://www.lr.pi.titech.ac.jp/%7Etakamura/pndic_ja.html)様の日本語版をデータベース化したデータです。
使用モジュールは`mod/judge_negaposi.py`になります。

### 単語分類表

どこで入手したか忘れてしまいました……。
使用モジュールは`mod/judge_category.py`になります。

## D18-2018.7.24フォルダ

1. [言語商会](https://www.jnlp.org/GengoHouse/top)様の[SNOW D18:日本語感情表現辞書](https://www.jnlp.org/GengoHouse/snow/d18)ページより、XLSXファイルをダウンロードします
1. `mod/dataset`フォルダ内に`D18-2018.7.24`フォルダを作成します
1. XLSXファイルの「作業者C」シートを`D18-2018.7.24.csv`として書き出し、`D18-2018.7.24`フォルダへ入れます
1. XLSXファイルの「感情分類」シートを`PositiveNegativeSymbol.csv`として書き出し、`D18-2018.7.24`フォルダへ入れます
	- Symbol(全て全角)の、(全て全角)は削除しました

使用モジュールは`mod/judge_kanjou.py`になります。このプログラムは[Pythonでちょっとだけ自然言語処理に挑戦](https://www.tdi.co.jp/miso/python-natural-language-processing)を改変したものです。