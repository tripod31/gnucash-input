import pandas
import argparse
import datetime
import sys
import common

"""
振替伝票入力形式excel→gnucash形式excel/csvに変換
input.xlsx→gnucash.xslx/gnucash.csv
"""

class AppException(Exception):
    pass

class Process:
    records=[]
    errors=[]

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

        #貸方データ
        rec = common.gnucash_empty_row()
        date = row["日付"]  #Timestamp型 or 文字列:%Y-%m-%d
        if type(date) is pandas.Timestamp: 
            date = date.strftime('%Y-%m-%d')   #文字列に変換
        rec["日付"] =date
        rec["番号"] =row["番号"]
        rec["説明"] =row["説明"]
        rec["勘定科目"] = row["貸方勘定科目"]
        rec["金額"] = row["金額"]
        self.records.append(rec)

        #借方データ
        rec =common.gnucash_empty_row()
        rec["日付"] =date  
        rec["番号"] =row["番号"]
        rec["説明"] =row["説明"]
        rec["勘定科目"]=row["借方勘定科目"]
        rec["金額"] = -row["金額"]
        self.records.append(rec) 

    def main(self):
        df = pandas.read_excel(
            args.in_excel_file,
            usecols="A:F",
            na_filter=False)    #空白セルをnanに変換しない
        
        #check rows
        self.errors.clear()
        for index,row in df.iterrows():
            no = row["番号"]
            if type(no) is int and no==0:
                #番号が"0"なら読み込みを中止する。空白行を全て読み込んで時間がかかる時があるため
                break
            self.check_row(row)
        if len(self.errors)>0:
            raise AppException("データチェックエラー")

        #process rows       
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
        print("{}行読み込みました".format(int(len(self.records)/2)))

if __name__ == '__main__':
    #引数
    parser = argparse.ArgumentParser()
    parser.add_argument('in_excel_file',    help="振替伝票入力形式のexcelファイル")
    parser.add_argument('out_excel_file',   help="gnucash形式のexcelファイル")   
    parser.add_argument('out_csv_file',     help="gnucash形式のCSVファイル")
    
    args=parser.parse_args()
    print("引数:{}".format(args))
    proc=Process()
    try:
        proc.main()
    except AppException as e:
        print(e)
        for err in proc.errors:
            print(err)
        sys.exit(1)
    sys.exit(0)
