gnucash_cols=[
    """
    gnucashインポート用csvの列名
    照合済="精"がデータにないとGnucash ver5で勘定科目の総合計が表示されない
    """
    "日付","番号","説明","勘定科目","金額","照合済","資金移動先勘定科目","資金移動先金額","資金移動先照合済"
]

def gnucash_empty_row():
    """
    戻り値
        gnucashインポート用csvの一行分の辞書。各列の値は空文字
        {"日付":"","番号":"",...}
    """
    return {col:"" for col in gnucash_cols}
