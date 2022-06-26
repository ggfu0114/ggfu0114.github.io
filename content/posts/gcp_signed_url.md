---
title: "Google cloud storage產生signed url的應用"
description: "本篇文章將會記錄如何在Google cloud platform上的storage產生signed url提供給使用者暫時的檔案存取權限"
author: "GGFU"
date: "2022-06-26"
Tags: 
- GCP
- storage
- signed URL
---

## Signed url的目的跟說明
這個功能主要是讓系統認可的使用者可以透過取的一個暫時的網址去存取雲端空間的權限

目前市面上有很多雲端提供者(cloud provider)，例如Google(GCP), Amazon, Azure...，他們都提供網路空間上開發者進行系統整合。

但是這些的空間通常因爲安全性(Security)的考量，都會將空間設定是私人，為的是防止有心人隨意上傳檔案。 但是會衍生出系統使用者(user)並沒有辦法上傳檔案，為了解決這個問題上 signed URL這個機制。

使用者必須先透過系統驗證機制(帳號/密碼, oauth...)讓系統知道使用者是誰之後，系統認可後為使用者製造出一段暫時性的網址，讓使用者去上傳或者是瀏覽檔案系統

在此篇文章中我們針對Google service的進行說明

## 如何做到Signed url的機制
使用者必須透過驗證機制讓伺服器知道他是合法的使用者，如此一來伺服器可以為使用者製造出一個暫時有權限的網址，並透過API回傳給使用者，使用者取的後就可以使用這個網址直接上傳到目標的空間。當有心人士想上傳不合法的檔案，會因為無取得系統的認可而不能上傳檔案(因為folder預設會是privated)。

## Debug過程
Send PUT http request to upload the file to a GCS bucket. And then the error message pop up on the chrome dev console.
:::danger
Access to XMLHttpRequest at 'https://storage.googleapis.com/xxxxxx' from origin 'http://127.0.0.1:5000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
:::
You have to update the bucket CORS policy by running following command.


```json=
[
    {
      "origin": ["http://127.0.0.1:5000/"],
      "method": ["GET","PUT"],
      "responseHeader": "*",
      "maxAgeSeconds": 3600
    }
]
```

客戶端所送出的header必須跟server端鼠藥加密的只只一致性否則會出現被拒絕的問題端鼠藥加密的只只一致性否則會出現被拒絕的問題


如果在整合系統跟Google storage時response都一直顯示問題的時候，我們可先固定傳輸產出的網址，然後填入不同參數的組合，看哪些headers是必要的
一個小技巧就是使用POSTman進行參數的試驗，當成功通過Google storage認可後，然後請POSTman幫忙轉譯出程式碼
![](https://i.imgur.com/bFkKtMC.png)




```shell=
gcloud init
```
