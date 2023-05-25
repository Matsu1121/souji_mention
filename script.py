# 当番表に基づいて、掃除当番の人をLINEでメンションする
# パソコンからLINEを自動操作する
# 当番表の名前とLINEの名前を一致させておく

import pandas as pd
import datetime

# 当番表を読み込む
df = pd.read_csv("掃除当番表.csv")

# 当日の日付情報
today = datetime.date.today()
mon = today.month
day = today.day

# 当日に該当する DataFrame
df_day = df[(df['月']==mon)&(df['日']==day)]

# タスクスケジューラで曜日で定期実行するが、念のため誤作動を防ぐ処理を入れる

if len(df_day)==1: # df_dayが空ではないとき
    # df_dayから当日の掃除当番の情報を取得
    [mem1, mem2, mem3, mem4, washer, checker] = df_day.loc[:, "当番1":"点検"].values[0]
    text1 = f"本日{mon}月{day}日の日曜掃除の担当者は\n"
    text2 = f"洗濯機は{washer}\n点検は{checker}さんです。\nがんばりましょう！"
    
    # LINEにメッセージを送る----------------------------------------------------------------------------
    
    # 必要ライブラリ
    import pyautogui
    import pyperclip
    import time

    #LINE起動
    time.sleep(2)
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('line')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(15) # 自動ログインできないとエラー

    # LINEを全画面表示に
    # 全画面にしないと失敗する（トークルームが開けない）
    pyautogui.hotkey('win', 'up')
    time.sleep(1)

    #検索ボックスに移動
    pyautogui.hotkey('ctrl', 'shift', 'f')
    time.sleep(1)

    #トークルーム名検索
    pyperclip.copy("日曜掃除")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)

    #トークルームを開く
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(3)

    #文字を書く
    pyperclip.copy(text1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    
    # メンションの処理
    for mem in [mem1, mem2, mem3, mem4]:
        pyperclip.copy(f"@{mem}")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        pyperclip.copy("くん\n")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        
    pyperclip.copy(text2)
    pyautogui.hotkey('ctrl', 'v')

    #送信
    pyautogui.press('enter')
    #--------------------------------------------------------------------------------------------------------
    print("実行に成功しました")
else: # df_dayが空であるとき
    print("実行に失敗しました")