---
title:  "Deploy s3 bucket by cloudformation - 進階版"
description:  "Deploy s3 bucket by cloudformation - 進階版"
author: "GGFU"
date: "2022-03-06"
Tags: 
- export
- stack
- cloudformation
- parameter`
---

#### 開發系統時部分的程式碼會參考到基礎建設的名稱，例如：S3 bucket自動部署創建出來的名稱，或是需要利用aws resource arn去做trigger lambda事件的綁定，都需要輸出佈建後的結果。


```javascript
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Create S3 bucket on AWS",
  "Parameters": {
    "StageName": {
      "Type": "String"
    }
  },
  "Resources": {
    "S3Test": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": {
          "Fn::Sub": [
            "paul-test-${StageName}",
            {
              "StageName": {
                "Ref": "StageName"
              }
            }
          ]
        },
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
            }
          ]
        }
      }
    }
  },
  "Outputs": {
    "S3Test": {
      "Description": "Information about s3 bucket name",
      "Value": {
        "Fn::Sub": [
          "paul-test-${StageName}",
          {
            "StageName": {
              "Ref": "StageName"
            }
          }
        ]
      },
      "Export": {
        "Name": {
          "Fn::Sub": [
            "${StackName}-S3Test-bucketname",
            {
              "StackName": {
                "Ref": "AWS::StackName"
              }
            }
          ]
        }
      }
    }
  }
}
```
<br>
`Parameters`:可以接收來自 aws cli 所輸入的參數，在執行cloudformation cmd時加參數加上`--parameter-overrides StageName="dev"`就可以將dev字串給傳入到Parameters的StageName。

`Fn::Sub`: 代表字串裡的變數，可用接下來的變數給取代。當字串不需要有變數取代時，可以簡單的利用`{ "Fn::Sub" : String }`描述即可。需要由變數替換的模板為`{ "Fn::Sub" : [ String, { Var1Name: Var1Value, Var2Name: Var2Value } ] }`。

> 查看部署的情況

利用describe-stack-events可以查看部署的情況，如果有部署錯誤，log大多會出現`"ResourceStatus": "CREATE_FAILED"`的字眼，當然系統也會整個自己rollback。

```shell
aws cloudformation describe-stack-events --stack-name paulteststack
```


#### 當部署完畢時，有指定需要輸出的參數可以利用`aws cloudformation list-exports`去取得部署時指定要輸出的參數值，下面的shell可以取出指定的name所對應的value數值，只要將字串export出去就可以做接下來的應用。

```bash
aws cloudformation list-exports --output text --query 'Exports[?Name==`'$StackName-S3Test'`].Value'
```

#### 如果不需要這些部署的基礎建設時，可以透過用aws cli去刪除stack，所有的服務就會都rollback刪除，不需要逐一的去刪掉各個服務(但是S3的服務可以例外，因為如果bucket裡面有資料檔的話，資源rollback無法刪除，需要手動去把S3的bucket刪掉)

```
aws cloudformation delete-stack --stack-name ${stack name}
```
