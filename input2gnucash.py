#!/usr/bin/env python3

import pandas
import argparse
import datetime
import sys
import common

"""
振替伝票入力形式excel→gnucash形式excel/csvに変換
input.xlsx→gnucash.xslx/gnucash.csv
入力ファイルに基本の列名以外の列名があれば、出力ファイルにも同じ列名、値で出力する
"""

#入力ファイルの基本の列名
BASIC_INPUT_COLS=[
    "日付","番号","説明","貸方勘定科目","借方勘定科目","金額"
]

class AppException(Exception):
    pass

class Process:
    def __init__(self):
        self.records=[]
        self.errors=[]
        self.additional_cols=[]  #入力ファイルの基本列名以外の列名
        self.empty_row = {}      #出力ファイルの１行分のdict。値は空

    def check_date(self,date):
        ret = True
        if type(date) is not pandas.Timestamp:            
            if type(date) is str:
                try:
                    dt = datetime.datetime.strptime(date,'%Y-%m-%d')
                except:
                    ret = False
            else:
                ret = False
        return ret

    def check_row(self,row):
        """
        入力ファイルの１行をチェック
        """
        date = row["日付"]
        if self.check_date(date) is not True:
            self.errors.append(f"{row['日付']}:日付の形式エラー(日付型or'%Y-%m-%d'以外)")
        if len(row["説明"])==0:
            self.errors.append(f"{row['日付']}:説明が入っていません")

    def process_row(self,row):
        """
        入力ファイルの一行を変換し出力
        row:    入力ファイルの一行
        """

        #出力データ一行分
        rec = self.empty_row.copy()
        date = row["日付"]  #Timestamp型 or 文字列:%Y-%m-%d
        if type(date) is pandas.Timestamp: 
            date = date.strftime('%Y-%m-%d')   #文字列に変換
        rec["日付"] =date
        rec["番号"] =row["番号"]
        rec["説明"] =row["説明"]
        rec["勘定科目"] = row["借方勘定科目"]
        rec["金額"] = row["金額"]
        rec["照合済"] = "清"
        rec["資金移動先勘定科目"] = row["貸方勘定科目"]
        rec["資金移動先金額"] = row["金額"]
        rec["資金移動先照合済"] = "清"        
        for col in self.additional_cols:
            rec[col]=row[col]
        self.records.append(rec)
    
    def main(self):
        #入力ファイル読み込み
        df = pandas.read_excel(
            args.in_excel_file,
            na_filter=False)    #空白セルをnanに変換しない
        
        #入力ファイルの列名で基本の列名以外の列名を、出力ファイルの列に追加
        for col in df.columns.to_list():
            if not col in BASIC_INPUT_COLS:
                self.additional_cols.append(col)
        if len(self.additional_cols)>0:
            print(f"以下の列名を追加します。[{','.join(self.additional_cols)}]\n")
        output_cols = common.gnucash_cols.copy()
        output_cols += self.additional_cols
        self.empty_row = {col:"" for col in output_cols}

        #入力ファイルの各行をチェック
        self.errors.clear()
        for index,row in df.iterrows():
            no = row["番号"]
            if type(no) is int and no==0:
                #番号が"0"なら読み込みを中止する。空白行を全て読み込んで時間がかかる時があるため
                break
            self.check_row(row)
        if len(self.errors)>0:
            raise AppException("データチェックエラー")

        #入力ファイルの各行を処理
        self.records.clear()
        for index,row in df.iterrows():
            no = row["番号"]
            if type(no) is int and no==0:
                #番号が"0"なら読み込みを中止する。空白行を全て読み込んで時間がかかる時があるため
                print("番号が0なので読み込みを中止します")
                break
            self.process_row(row)
        df = pandas.DataFrame(self.records)
        df.to_excel(args.out_excel_file,index=False)
        df.to_csv(args.out_csv_file,index=False)
        print(f"{len(self.records)}行出力しました")

if __name__ == '__main__':
    #引数
    parser = argparse.ArgumentParser()
    parser.add_argument('in_excel_file',    help="振替伝票入力形式のexcelファイル")
    parser.add_argument('out_excel_file',   help="gnucash形式のexcelファイル")   
    parser.add_argument('out_csv_file',     help="gnucash形式のCSVファイル")
    
    args=parser.parse_args()
    print(f"引数:{args}")
    proc=Process()
    try:
        proc.main()
    except AppException as e:
        print(e)
        for err in proc.errors:
            print(err)
        sys.exit(1)
    sys.exit(0)
