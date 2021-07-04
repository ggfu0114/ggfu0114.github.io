# S3 multipart uplaod prsigned url教學


當系統需要做續傳功能或大檔上傳的功能時，S3提供multipart upload的功能，可將檔案切分上傳，最後到S3再進行合併。主要分成3步驟：

- Multipart upload init
- 上傳一個或多個parts
- Multipart  upload complete


### 上傳初始化

檔案要上傳到S3時，需指明當這個 multipart upload 完成組合成一個 object 後，object 的 key 值為何，若希望以 multipart upload 建立的 object 帶有自訂的 metadata，亦須在 multipart upload 初始化時提供。成功初始化後，S3會建立一組 upload ID 當成未來上傳為此 object 的依據。
```xml=
<?xml version="1.0" encoding="UTF-8"?>
<InitiateMultipartUploadResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Bucket>test201705021548</Bucket>
    <Key>hello.jpg</Key>
    <UploadId>QAUmLo15J46MyspVk6PgCPg7C1yk9RdOR2XfsdwEe2xDVS33HTh.cAJzFfwcug--</UploadId>
</InitiateMultipartUploadResult>
```

> 操作步驟

1. 為 init multipart 的需求產出數位簽章。
```javascript
var StringToSign = "POST" + "\n" +
    "" + "\n" +
    "" + "\n" +
    new Date().toUTCString() + "\n" +
    "/test201705021548/hello.jpg?uploads";
```

init成功時，S3會回傳對應的 `upload ID`

2. 利用 Postman 去發送 init 的 request。Header一樣需要帶上 Authorization: AWS {AWSAccessKeyId}:{Signature} 資訊。 url 需要帶上 `?uploads` 字串。

```shell=
curl -X POST \
  'https://s3-ap-northeast-1.amazonaws.com/test201705021548/hello.jpg?uploads=' \
  -H 'authorization: AWS AKIAIUHT2BNZP65ADZKQ:WrvZSAcl9BDPKQUuiY2uBpeN9UM=' \
  -H 'cache-control: no-cache' \
  -H 'date: Thu, 11 May 2017 05:47:14 GMT' \
  -H 'postman-token: 0e6bd8a1-70e2-5e8a-7f2e-0f8a45a6fb8f'
```


### 上傳部份檔案
此操作的 request 需要帶有 upload ID。在上傳每個 part 需指定一個 part number 作為識別。若對一個 multipart upload 上傳重複 part，較早上傳的 part 會被覆蓋。除了作為識別，part number 決定了當 multipart upload 完成為 object 時，每個 part 排列組合的順序，Part number 的合法範圍是 1 到 10000。

> 操作步驟

1. 為各個上傳 part 做數位簽章。重點在於要填上 `partNumber` 和 `uploadId`。第一的參數字己指定，第二個參數再一個步驟會產出。
```javascript
var StringToSign = "PUT" + "\n" +
    "" + "\n" +
    "" + "\n" +
    new Date().toUTCString() + "\n" +
    "/test201705021548/hello.jpg?partNumber=1&uploadId=pDIXIj7uWNJuxuUgXLw5jp3QgbXoRfuopriYQMkP4d_3BCpxgjt8Y.wPsJMCFpZr3oU1a4JFa7R2KsC9J9R7htCJtuBeshRVLDInTMYk97QyxENxM8tLPH1KiY8PBvSkcsP8r9uj8oJUqm_O5jbcXQ--";

```
2. ==ps== 如果是利用 Postman 去上傳各個部份的資料。這邊需要多增加`Content-Length`的 Header 參數，假如是用javascript的httprequest會自動付在Header上。
![](https://i.imgur.com/IFOC0Y5.png)

上傳檔案成功時，S3會回傳對應的Header需要的有 ETag 欄位

![](https://i.imgur.com/ZvIVyge.png)
==Note== 如果用前端想取得 RespondHeader 裡的 ETag 欄位值，出現 Refused to get unsafe header "etag" 錯誤時，請調整 S3 bucket 的 CORS configuration 設定值，加上 `<ExposeHeader>ETag</ExposeHeader>`

### 合併並完成上傳

> 操作步驟

1.為結束上傳且合併做數位簽章
```javascript

var StringToSign = "POST" + "\n" +
    "" + "\n" +
    "" + "\n" +
    new Date().toUTCString() + "\n" +
    "/test201705021548/hello.jpg?uploadId=pDIXIj7uWNJuxuUgXLw5jp3Qpxgjt8Y.wPsJMCFpZr3oU1a4JFatCJtuBxENxM8tLPH1KiY8PBvSkcsP8r9uj8oJUqm_O5jbcXQ--";
```
2.利用 Postman 去執行 object 合併。注意，在這邊的 Content-Length 長度並不是各個檔案加總的總長度，而是要合併的XML的字串長度，如下面第2張圖的長度為141。 為了傳送 raw 的 XML 合併資訊，所以我先用筆記本將圖二的資訊寫下來，然後再用 binary 的檔案夾帶。
![](https://i.imgur.com/HThEcDE.png)


```xml=
<CompleteMultipartUpload>
    <Part>
        <PartNumber>1</PartNumber>
        <ETag>37f6dc6369d67c211a9a0d9f3334208d</ETag>
    </Part>
    <Part>
        <PartNumber>2</PartNumber> 
        <ETag>4a2c7c32e54f36c9bdc9bdf23d169a53</ETag>
    </Part>
</CompleteMultipartUpload>
```

```xml=
<CompleteMultipartUploadResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Location>https://s3-ap-northeast-1.amazonaws.com/test201705021548/hello.jpg</Location>
    <Bucket>test</Bucket>
    <Key>test.jpg</Key>
    <ETag>"69047f1fdf14e93328ff8319083a0e27-2"</ETag>
</CompleteMultipartUploadResult>
```

:::danger
### 利用 Javascript 發 request 時，Header 不能帶 Date 參數
因為 Date 是內建的 Header 參數，所以不允許使用者去覆蓋參數，AWS 提供另一種變數 `x-amz-date` 當時間參數，所以計算的字串會變成以下，將 Date 的資訊列給空白下來。
```javascript
let string_to_sign = method_str + "\n" +
            content_md5_str + "\n" +
            content_type_str + "\n" +
            "\n" +
            "x-amz-date:"+date_str+"\n"+
            canonicalized_resource_str;
```

:::

**[S3 multipart upload presigned 教學文件](http://s3help.cloudbox.hinet.net/index.php/api-multipart-upload-overview)**
**[S3 multipart upload cli 教學文件](https://aws.amazon.com/premiumsupport/knowledge-center/s3-multipart-upload-cli/)**



###### tags: `S3`, `multipart`, `presign`