# GnuCash-input
GnuCashは、フリーの会計ソフトです。https://www.gnucash.org/  
GnuCashの取引データをExcelで入力するために作成しました。GnuCashの取引入力画面で入力するより効率的だと思います。Excelで入力すれば、同じパターンの取引データをコピーして入力する等できて効率的です。  
CSVファイルからGnuCashにインポートできます。しかし、GnuCash形式のCSVは貸方と借方が２行に分かれており、データを作成しづらいです。このため、振替伝票形式（独自形式）のExcelファイルをpythonでGnuCash形式に変換するプログラムを作成しました。
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
CSVの列名とGnuCashのデータ項目の対応をリストボックスから設定する必要があります。
![gnucash-input](https://github.com/tripod31/GnuCash-input/assets/6335693/4896bf18-b110-48d7-b737-93b6e8ba5c6d)

## Excelファイル
サンプルはinput.xlsxです。各列は以下の通り  
|列名|
|--|
|番号|
|日付|
|貸方勘定科目|
|借方勘定科目|
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
