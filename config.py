"""グローバル変数"""

"""
Parameters
----------
config.threshold_val : float
    score 値と比較する閾値を保持
config.threshold_len : int
    閾値以上の score の連続回数と比較する閾値を保持
config.fill_gap : int
    閾値以下をスルーする回数を保持。メディアンフィルタてきな
        
"""
threshold_val = 0.0      # score valueの閾値
threshold_len = 0    # score lengsの閾値
fill_gap = 0          # score gapの閾値
keyword = ""
isFilter = True
isKeyword = False
