Title: AWS S3 REST 數位簽章與驗證
Description: 利用數位簽章讓使用者可以透過 api resquest 去做身份認可(identity)並操作S3裏面的物件
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/


# AWS S3 REST簽章與驗證
- 假設在S3裡的物件只設定給 "authenticated AWS user" 操作，那我們要如何利用數位簽章讓使用者可以透過 api resquest 去做身份認可(identity)並操作S3裏面的物件。
- 假設在S3上我們有一個name為 wisigntest 的bucket，裏面存在一個名為hello.jpg的物件，設定為 "authenticated AWS user" 可以R/W。我們將紀錄如何使用API去存取S3物件。

> 簡易瀏覽物件
```
GET /hello.jpg HTTP/1.1
Host: https://wisigntest.s3-ap-northeast-1.amazonaws.com
Date: Fri, 28 Apr 2017 05:56:29 GMT

Authorization: AWS AKIAIOSFODNN7EXAMPLE:frJIUN8DYpKDtOLCwo//yllqDzg=
```
下面是我用Postman去讀取S3檔案的畫面
![](https://i.imgur.com/dnJRA2I.png)

>The Authentication Header

下面的格式是主要傳送給 API 的 Header 上要添加的 Authorization 資訊，透過Signature，AWS可以驗證此次的操作是否有效。
```
Authorization: AWS {AWSAccessKeyId}:{Signature}
```
下面是 Nodejs 計算的Signature程式碼
```javascript
var crypto = require("crypto");

// from IAM role
var secret_access_key = '64nd6BY7gTPDspq54gQcRth5dvORNdDvqL4BZ5zd';
var access_key_id = 'AKIAIUHT2BNZP65ADZKQ'

var StringToSign = "GET" + "\n" +
    "" + "\n" +
    "" + "\n" +
    new Date().toUTCString() + "\n" +
    "/wisigntest/hello.jpg";


var Signature = crypto
                .createHmac('sha1', secret_access_key)
                .update(StringToSign)
                .digest('base64');

console.log("\n=====Signature=====");
console.log(Signature);
console.log("\n=====StringToSign=====");
console.log(StringToSign)
```
所以 Signature 會因為每分每秒時間的變動，加上每次要操作的行為不一樣而有不同的結果。如果 Header 上Date的數值跟當前的時間差太遠會產生出RequestTimeTooSkewed Error(如下圖)，最多只能延遲15 minutes 進行操作。一旦過期就只能再重新產生一組新的操作。
```yaml=

<?xml version="1.0" encoding="UTF-8"?>
<Error>
    <Code>RequestTimeTooSkewed</Code>
    <Message>The difference between the request time and the current time is too large.</Message>
    <RequestTime>Fri, 28 Apr 2017 07:01:06 GMT</RequestTime>
    <ServerTime>2017-04-28T07:17:20Z</ServerTime>
    <MaxAllowedSkewMilliseconds>900000</MaxAllowedSkewMilliseconds>
    <RequestId>A1CC38F343F62CB3</RequestId>
    <HostId>mJYpxdY5MthZwY4NUeF/MTIcJbYPpZ+6+haAfHkn40AX32XMrP618pzOv+MsZvAE965jaM1OgCk=</HostId>
</Error>
```
> 利用 API form 上傳檔案到 S3

- 如果今天有一個檔案叫 hello1.js要上傳到S3的 wisigntest bucket 裡，可以依照以下步驟去執行


![](https://i.imgur.com/KFIxuR7.png)
![](https://i.imgur.com/Y1zmUks.png)

在 Postman 上做發送照片的 request，Header參數上依然要填上 Authorization, Date參數，Content-Type填上"text/plain"。

```javascript
var StringToSign = "PUT" + "\n" +
    "" + "\n" +
    "text/plain" + "\n" +
    new Date().toUTCString() + "\n" +
    "/wisigntest/hello1.jpg";
```

只要把上面的 "StringToSign" 變數改成上面所序，就可以產出正確的 Signature 了

> 沒有 Header 的 request authentication

此外 S3 提供不需帶 Header 的存取方法。基本上是將Date用Expires取代，然後所有的參數都放置在 URL 上。例如下方的 URL，主要的參數有 AWSAccessKeyId, Expires, Signature。AWSAccessKeyId 跟 Signature 的產出原理一樣，Expires 則是當前的 Timestamp 再加上預期 URL 失效的時間。 

:::success
https://wisigntest.s3-ap-northeast-1.amazonaws.com/hello.jpg?AWSAccessKeyId=AKIAIUHT2BNZP65ADZKQ&Expires=1493368109&Signature=xLO3tdF%2FAutv%2BYinCfA7G8C157E%3D
:::

產出 Signature 需要將 Date 變數取代為預期失效的 Timestamp 時間。下面的例子即是當前時間加上 600 Seconds 時，URL 就會失效。



```javascript
var StringToSign = "GET" + "\n" +
    "" + "\n" +
    "" + "\n" +
    parseInt(Date.now() / 1000+600) + "\n" +
    "/wisigntest/hello.jpg";
```

- 參考資料
[AWS S3 Signing and Authenticating REST Requests](http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html )




###### tags: `S3`, `presign`, `REST`, 