# GnuCash-input
GnuCashは、フリーの会計ソフトです。https://www.gnucash.org/  
GnuCashの取引データをExcelで入力するために作成しました。GnuCashの取引入力画面で入力するより効率的だと思います。Excelで入力すれば、同じパターンの取引データをコピーして入力する等できて効率的です。  
CSVファイルからGnuCashにインポートできます。しかし、GnuCash形式のCSVは貸方と借方の金額を別の列に書く等、データが作成しづらいです。このため、振替伝票形式（独自形式）のExcelファイルをpythonでGnuCash形式に変換するプログラムを作成しました。
## 動作確認環境
* Windows11
* python3.11.1
* GnuCash5.4
## 必要ライブラリ
* pandas
## 取引の入力手順 
1. Excelで取引を振替伝票形式（独自形式）のExcelファイルへ入力 
2. pythonでExcelファイルをGnuCashインスポート形式CSVに変換(このプログラムを使用)
3. GnuCashでCSVファイルをインポート  
CSVの１行目をスキップする設定にします。  
CSVの列名とGnuCashのデータ項目の対応をリストボックスから設定する必要があります。  
列名は以下の通りで、CSVの列名とGnuCashのデータ項目名は同じです。  

|列名|
|--|
|日付|
|番号|
|説明|
|勘定科目|
|金額|
|照合済|
|資金移動先勘定科目|
|資金移動先金額|
|資金移動先照合済|

![gnucash-input](https://github.com/tripod31/gnucash-input/assets/6335693/839e82ba-f852-4469-bb7a-c1da6d8dadd5)

## Excelファイル
サンプルはinput.xlsxです。各列は以下の通り。  
これ以外の列名の列があれば出力ファイルにそのまま出力されます。  
|列名|
|--|
|番号|
|日付|
|借方勘定科目|
|貸方勘定科目|
|金額|
|説明|
## 実行方法
```
usage: input2gnucash.py [-h] in_excel_file out_excel_file out_csv_file

positional arguments:
  in_excel_file   振替伝票入力形式のexcelファイル
  out_excel_file  gnucash形式のexcelファイル
  out_csv_file    gnucash形式のCSVファイル

optional arguments:
  -h, --help      show this help message and exit
```
例：  
```
>python input2gnucash.py input.xslx gnucash-input.xslx gnucash-input.csv
```
