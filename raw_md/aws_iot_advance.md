Title: AWS IoT | 進階資訊分享
Description: 在 AWS IoT的資源上，有部份的 topic name是被保留，並寫說明用IoT service 驅動lambda.
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/

# AWS IoT - 進階

### IoT reserved topic

- 在 AWS IoT的資源上，有部份的 topic name是被保留。

`$aws/events/presence/connected/#` : 如果有任何的使用者連上 IoT 就會推播訊息到這個 Topic 
` $aws/events/presence/disconnected/#`: 如果有任何的使用者斷線,就會推播訊息

- 這個是當使用者 connected/disconnected 推播到 topic 裡的訊息範例
```javascript=
{
    "clientId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    "timestamp": 1460065214626,
    "eventType": "connected",
    "sessionIdentifier": "00000000-0000-0000-0000-000000000000",
    "principalIdentifier": "000000000000/ABCDEFGHIJKLMNOPQRSTU:some-user/ABCDEFGHIJKLMNOPQRSTU:some-user"
}
```

`$aws/events/subscriptions/subscribed/#`: 如果有任何的使用者訂閱了任何的 topic就會推播訊息到這個topic
`$aws/events/subscriptions/unsubscribed/#`：  如果有任何的使用者解訂閱了任何的 topic就會推播訊息

- 這個是 subscribed/unsubscribed 推播的訊息範例
```javascript=
{
    "clientId": "186b5",
    "timestamp": 1460065214626,
    "eventType": "subscribed" | "unsubscribed",
    "sessionIdentifier": "00000000-0000-0000-0000-000000000000",
    "principalIdentifier": "000000000000/ABCDEFGHIJKLMNOPQRSTU:some-user/ABCDEFGHIJKLMNOPQRSTU:some-user"
    "topics" : ["foo/bar","device/data","dog/cat"]
}
```
:::info
#### 同時要聆聽相同 Topic 底下不同的子 Topic 可用 + 號串聯，例如：
`$aws/events/subscriptions/+/#`: 可以同時聆聽到 connected, disconnected, subscribed, unsubscribed ...的訊息
`company/+/member`： + 號可以是任意的字串，只要符合這個 Topic 的 name 的規則，都可以收到資訊
:::


### IoT trigger lambda

IoT 要 trigger lambda 需要先定義 rule，透過 rule 的定義去執行 Lambda和傳送對應的參數，rule包含兩個主要資訊
`query statement` 這個參數是拿來定義要傳入 lambda 的規則，例如：

```sql=
SELECT * as data FROM '$aws/events/presence/connected/#' 
/* 將所有 IoT 所收到的資料都傳進去 lambda 的參數裡 */

SELECT * as data, topic() as topic, clientid() as cliendId, timestamp() as timestamp FROM '+/updateStatus'
/* 所有傳送到 +/updateStatus 的資料，我們將 data, topic,clientid, ts 都傳入 lambda*/

```

`actions` 用來定義要將哪隻 Lambda 驅動
- 透過 AWS IoT 可手動選擇驅動的 Lambda
![](https://i.imgur.com/oUCBSsh.png)

- 或是，用的是 serverless 套件去佈署 AWS resources，下面是一個佈署範例：
```yaml=
playerUpdateStatus:
    handler: handler.handler_function
    name: updateDeviceStatus
    description: IoT Device state
    events:
      - iot:
          name: UpdateDeviceRule
          sql: "SELECT * as data FROM '$aws/events/subscriptions/subscribed/#'"
          description: "IoT Update Rule"
```

###### tags: `AWS`, `IoT`, `lambda`, `topic`