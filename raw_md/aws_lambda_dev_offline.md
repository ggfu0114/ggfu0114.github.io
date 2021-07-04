Title: Serverless offline 開發設定 - 基礎篇
Description: 為了加速開發的效率，開發過程中不會想要每次都佈署到AWS做測試或開發。Serverless offline套件可以解決這件事情。透過模擬 AWS λ and API Gateway ，開發者在本機端就可以run一個的server去模擬再AWS服務的情況
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/


# Serverless offline 開發設定 - 基礎篇
> 說明

為了加速開發的效率，開發過程中不會想要每次都佈署到AWS做測試或開發。Serverless offline套件可以解決這件事情。透過模擬 AWS λ and API Gateway ，開發者在本機端就可以run一個的server去模擬再AWS服務的情況。

> 前置作業

需要事先安裝過 serverless package
` sudo npm install serverless -g `
安裝serverless offline套件
` npm install serverless-offline --save-dev `

> 使用方法

在原本專案的serverless.yml上添加程式碼
#### plugins
```xml=
plugins:
  - serverless-offline
```
 
 
#### server conf
    
將server在 3000 PORT 開啟; 開放所有的 IP 都可以存取
```xml=
custom:
  serverless-offline:
    host: "0.0.0.0"
    port: 3000
```
    
 

在Terminal上啟動 serverless offline server
`serverless offline start`
接著就可以用各種工具去發出request做開發測試

:::danger

#### 執行API request出現錯誤


```javascript
{
    "statusCode": 400,
    "error": "Bad Request",
    "message": "Invalid cookie value"
}
```
- 經過測試，如果將IP綁在127.0.0.1或是沒有設定(系統預設為localhost)的話會出現access error，這個問題只要將 IP 綁在 0.0.0.0 然後 request 的 host 為指定 IP 就可以解決這個問題，ex : http://192.168.1.101/dev/test 
:::


###### tags: `AWS`, `offline`