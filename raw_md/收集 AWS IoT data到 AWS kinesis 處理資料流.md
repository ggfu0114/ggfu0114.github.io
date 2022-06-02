Title: 收集 AWS IoT data到 AWS kinesis 處理資料流
Description: 收集 AWS IoT data到 AWS kinesis 處理資料流
Authors: GGFU
Date: 03/06/2022
Tags: 
base_url: https://ggfu0114.github.io/

# 收集 AWS IoT data到 AWS kinesis 處理資料流

- 使用AWS IoT服務來開發大量的資料傳輸系統，主要是想彙整資料或是做數據分析，AWS同樣提供資料串流的分析服務 `kinesis`. kinesis服務裡面有三個類別，Data Streams, Data Firehose, Data Analytics. 
1. `Data Streams`: streams 這個服務其實就有點類似 Kafka. 在IoT mqtt的protocol下，publish/subscribe之間系統是不會保存任何傳遞的資料。所以一但需要做資料流分析時，需要將收到的資料存在Message Queue裡，kinesis streams就擔任這個初階的角色，stream可以搭配firhorsec，analytics，lambda...一起使用。


2. `Data Firehose`: firehose可以將stream的資料倒至其他AWS的服務，例如： S3, Redshift...，firehose服務裡提供transformation功能將資料整理成需要的格式。


3. `Data Analytics`: 利用收到的data stream，只要提供需要sql程式，設定好Source(data stream)與Destination，AWS就會提供即時分析服務。




> IoT trigger Kinese stream
- 只要在IoT的Service上建立rule，只要推送資料到設定的topi就會將資料導入Kinese stream。
- 選定 `Send messages to an Kinesis Stream` 就可以在符合Rule時將資料導入data stream
![](https://i.imgur.com/jYISnxa.png)
- 選定預先創立好的stream，設定Partition key，還有執行角色就完成
![](https://i.imgur.com/nFr6vaZ.png)
> Partition key說明

- 利用Partition key，IoT的資料可以藉由group的方式去將資料分配的儲存在stream的shards裡面，最容易的方式是用網頁上提供的function: newuuid()，去隨機產出亂數平均的儲存資料，或是利用IoT的資料裡面的Key直做group。

```javascript
[{'key':'a1', 'value':1}, {'key':'a2', 'value':2}, {'key':'a1', 'value':3}]
```
如果Partition key填入`${key}`，那麼第1,3比資料會被送到stream裡的同一個shard，2則被送到另一個shard。

> trigger lambda處理收集好的batch資料
1. shard只由一個lambda服務 pull
2. 多shard由多個lambda執行task, semphore問題 
###### tags: `aws`, `iot`, `kinesis`, `lambda`, `batch`

