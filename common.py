gnucash_cols=[
        "日付","番号","説明","勘定科目","金額"
]

def gnucash_empty_row():
    """
        returns:
            {"日付":"",...}
    """
    return dict(list(map(lambda x:(x,""),gnucash_cols)))
