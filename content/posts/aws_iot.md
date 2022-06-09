---
title: "AWS IoT介紹"
description: "裝置可以透過 certificates 去做驗證,連接上AWS IoT service做系統整合應用"
author: "GGFU"
date: "2020-12-31"
Tags: 
- AWS
- IoT
- policy
---


# AWS IoT

> 說明

![](https://i.imgur.com/khnUOLr.png)


- certificate：裝置可以透過 certificates 去做驗證，保證使用 IoT 的溝通上 security 是沒有任何問題的。除了certificates之外，也可以透過IAM權限，Congnito 的權限控管去操作 IoT 的  resources (如上圖)。


1. 利用 AWS IoT 提供的 sdk 可以在 AWS resource 內產出一組 certificate， 裏面包含的資訊會有`certificate pem` `keyPair(a pair of public & private key)` `certificateId & ARN`

2. 取得憑證後，需要在憑證上套用policy，policy就好像規定這拿著這隻憑證鑰匙可以進哪個門，不能進哪個門，以達到 AWS IoT 的 resource 控管。

### Policy設定
- 以下的這個 Policy設定代表使用者只要有合理的 certificates，就可以針對IoT上所有的resources 做連線，推播，接收的動做，沒做任何的限制管控，如果要限制使用者能力有下面另外一個範例

```javascript
{
  "Version": "2012-10-17",
  "Statement": [{
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Subscribe",
        "iot:Connect",
        "iot:Receive"
      ],
      "Resource": ["*"]
    }]
}
```

- 如果想讓使用者只能針對自己 CertificateId 的 topic 操作，policy 就要修改成以下的方式，利用 `${iot:CertificateId}` 的變數，AWS IoT 會去檢查裝置端連線時所使用的憑證，達到每個憑證只能操作對應憑證 ID 的 Topic，降低資訊被竊取的風險。


```javascript
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": "arn:aws:iot:ap-northeast-1:1234:topicfilter/${iot:CertificateId}"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:ap-northeast-1:1234:client/${iot:CertificateId}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Receive"
      ],
      "Resource": "arn:aws:iot:ap-northeast-1:1234:topic/${iot:CertificateId}"
    }
  ]
}
```

connect 的 policy 要跟操作 IoT resources 要分開寫，因為 connect 是針對 client resource 操作，但是其他的動作是針對 IoT 上的 topic resource 做操作，如果都在一條 statement 會導致錯誤。

