Title: Flask 要如何做測試
Description: 如何利用python unittest去測試開發好的web application讓系統更加穩定
Authors: GGFU
Date: 01/07/2021
Tags: 
ID: flask_unittest
base_url: https://ggfu0114.github.io/

# flask-unittest

## 為什麼需要寫測試

寫測試對許多初學者來說，會覺的非常費時且沒有必要，心裡想著，我都親自測試過了，程式執行起來沒有什麼問題，為什麼需要花很多時間測試呢？

對於這個疑問，最簡單的回答是，寫測試大多是為了`未來`

專案只有幾個情況下比較不需要寫測試：
1. 專案只會執行幾次就不再使用
2. 還在初期的規規劃跟實驗的狀態(POC)

當你的專案有以下的情況,測試程式碼就會勢在必行：
1. 越寫多程式碼,程式的複雜度跟耦合度漸漸變高時
2. 專案成員變多,程式碼改動變頻繁的時候
測試程式碼就變的極為重要
測試可以讓你所開發的程式碼不會受到別人的改動而遭受影響(Side effect),當然要配合Dev Ops的CI/CD 效果才會比較好.


> Pytest vs. unittest

在Python內建的模組裡有包含了測試，所以不需要安裝任何第3方套件就可以載入`unittest`模組來寫測試.
我個人式比較常用`pytest`.

`pytest`的好處是：
1. 提供比unittest更多的輔助工具來幫助測試
2. 所有用unitest語法寫的測試程式碼,都可以用pytest來執行

## 執行測試

在Terminal上面執行pytest指令並加上一個資料夾，pytest就會自動去收集這個資料夾裡面帶有`test_*.py` 或是 `*_test.py`檔名的測試並執行

```sh
pytest tests -v -s
```
`-v`: 描述詳細的測試訊息
`-s`: 顯示程式碼裡面印出來的資訊


## Unittest Mock

`Mock` 的功能對於測試非常的重要，例如：A function 裡面包含執行 B, C, D功能，但是在測試 A 功能時，我們並不想要測試 C 功能，只需要 bypass C 功能，這個時候 Mock 功能就派上用場.

`patch` 是Mock裡面所提供的一個功能，它可以去取代掉原本功能的過程，例如：

```py
@patch('func.MathFunc.get_random_point')
def test_multiply(self, mock_func):
    mock_func.return_value = (8, 6)
```
以上的程式碼代表，原本的get_random_point功能想要被取代，不論原本那個功能裡面的邏輯是什麼, 最終回傳值就一定會是一個tuple包含8,6這兩個值。


## Flask test

利用Flask在寫Web Application時, 通常會進行API test. 意思就是，我們會在API request中傳入參數, 並預期會有什麼response結果。
```py
app.test_client()
```
在 Flask 的app裡提供test_client功能，當執行後此function會回傳一個專門拿來測試用的client，我們的測試項目就可以利用這個client去發送測試的request.

利用test_client測試時，我們不需要特地自己去執行flask server.

```py
client.get('/')
```
使用test client 我們可以針對server所有的網址跟method(get, post, update, delete)進行測試
