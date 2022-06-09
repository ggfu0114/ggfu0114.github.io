---
title: "Deploy s3 bucket by cloudformation"
description: "Deploy s3 bucket by cloudformation"
author: "GGFU"
date: "2022-03-06"
tags: 
- AWS
- S3
- cloudformation
- template
- batch`
---

#### 預先準備
需要先把 aws cli 給裝起來

 利用CLI可以把預先寫好的基礎建設結構佈署到AWS上，下面是簡單部署一個S3的bucket範例。

```shell=
aws cloudformation deploy --stack-name paulteststack --template-file ./s3-create-template.json
```


`--stack-name`: 想要deploy到哪一個cloudformation stack裡 
`--template-file`:  template 檔案的所在位置
還有很多參數可以設定，詳情可以參考 [create-stack](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack.html)
 
 <br>
#### 創立基礎建設所需要的資源描述檔，以下是一個最簡單的建立s3 bucket的描述檔，只要修改`BucketName`為自己所想要命名的名稱，再將檔案存成json就可以開始部署了，bucket名稱不可以跟既有的名稱重複(global)。


```javascript
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Create S3 bucket on AWS",
  "Resources": {
    "S3Test": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "paul-test-1495611707"
      }
    }
  }
}
```


#### template 可以依照情境進行更進階的調整，例如調整bucket的CROS讓外部的前端程式可以進行存取。


```javascript
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Create S3 bucket on AWS",
  "Resources": {
    "S3Test": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "paul-test-1495611707",
        "AccessControl": "PublicReadWrite",
        "CorsConfiguration": {
          "CorsRules": [
            {
              "AllowedHeaders": [
                "*"
              ],
              "AllowedMethods": [
                "GET"
              ],
              "AllowedOrigins": [
                "*"
              ],
              "ExposedHeaders": [
                "Date"
              ],
              "Id": "myCORSRuleId1",
              "MaxAge": "3600"
            },
            {
              "AllowedHeaders": [
                "x-amz-*"
              ],
              "AllowedMethods": [
                "DELETE"
              ],
              "AllowedOrigins": [
                "http://www.example1.com",
                "http://www.example2.com"
              ],
              "ExposedHeaders": [
                "Connection",
                "Server",
                "Date"
              ],
              "Id": "myCORSRuleId2",
              "MaxAge": "1800"
            }
          ]
        }
      }
    }
  }
}
```

`AccessControl`: PublicReadWrite代表所有的人都可以針對這個bucket進行讀寫的操作

`AllowedHeaders`: 這個欄位代表只要是get的method,header都不做任何的限制

`AllowedMethods`: 如果只填get那麽post, delete...都無法執行

`AllowedOrigins`: 代表不會限制任何網站來存取這個檔案

`ExposedHeaders`: respond header可公開的標頭

`MaxAge`: 瀏覽器會cache S3的preflight OPTIONS多久，重複的request就不會送到s3

更多不同的進階應用都可以在AWS官網上找到 [s3 cloudformation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
