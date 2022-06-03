Title: Flask 第一個 APP(初學入門)
Description: 如何利用python flask寫一個最簡單的Web server並執行網站
Authors: GGFU
Date: 01/07/2021
Tags: 
ID: flask_first_app
base_url: https://ggfu0114.github.io/



# Flask 第一個 APP

學了Python卻不知道可以應用在哪裡?
這個影片包含了
1. 如何寫一個最簡單的Web server
2. 做好的網站要怎麼執行
3. 我想要Debug該怎麼做

點選以下影片觀看↘↘

[![Flask 第一個 APP](https://img.youtube.com/vi/eN8s9pHRsNM/0.jpg)](https://youtu.be/eN8s9pHRsNM)

設定或開發環境遇到問題了? 

請看影片：[Python的開發環境設定](https://www.youtube.com/watch?v=7AO9TYd3d-c)

***

## 檔案介紹
`main.py`: 整個Flask APP 主要的進入檔案

`requirement.txt`: 執行APP所需要的相依套件(開發工程師不可能所有功能都自己獨立製作，所以需要很多Open Source的套件來輔助，完成一套用的系統)

## 程式碼解說
```py
@app.route('/')
```
URL的入口點，當使用者打錯網址時， APP沒有辦法找到對應的function來處理時，就會出現 *404 not found* 的錯誤。


```py
return "<div>Hello World, gFu.<div>"
```
當使用者連上正確的URL時，APP就會幫忙處理資料，但是這個簡單的範例並沒多加複雜的邏輯，只有回傳單純的html元素給使用者。
