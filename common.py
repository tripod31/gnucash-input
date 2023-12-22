gnucash_cols=[
    #照合済="精"がデータにないとGnucash ver5で勘定科目の総合計が表示されない
    "日付","番号","説明","勘定科目","金額","照合済"
]

def gnucash_empty_row():
    """
        returns:
            {"日付":"",...}
    """
    return dict(list(map(lambda x:(x,""),gnucash_cols)))
