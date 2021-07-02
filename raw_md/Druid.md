# Druid
## Druid Terms
`multi-tenant`: a single instance of software runs on a server and serves multiple tenants
`OLAP`: Online analytical processing, is an approach to answering multi-dimensional analytical (MDA) queries swiftly in computing
`SaaS`: a software distribution model in which a third-party provider hosts applications and makes them available to customers over the Internet
`ROLL-UP`: 將原始數據在匯入資料庫時就進行彙整處理
## Scenario
1. 資料已經整理好，不需要更新操作
2. 不需要做表格的join
3. 對於資料時間維度要求比較高的工作
4. 即時性極重要的project

## External Dependencies
`Zookeeper`: cluster內部溝通資訊所用
`Metadata Storage`: 儲存segment的meta data和configuration，提供coordinator node去調配segment的的載入情況
`Deep Storage`: segment的永久儲存空間，提供Historical node去下載segment

## Key Features
* Sub-second OLAP Queries
* Real-time Streaming Ingestion
* Power Analytic Applications
* Cost Effective
* Highly Available
* Scalable

extremely low latency queries
powering applications used by thousands of users
not support full text search(vs Elasticsearch)

1. **Real-time Nodes**
- 用於儲存Hot data，並定期地將數據切分成segment轉移到Historical Node
2. **Historical Nodes**
- 於Deep Storage載入segment並回應Broker Nodes的請求
- 採用無共享架構設計
3. **Broker Nodes**
- 接收外部的query request
- 透過查詢 Zookeeper將請求劃分成 segments分別轉给 Historical和 Realtime Nodes
- 聚集和合併查詢结果，並返回查詢結果给外部
4. **Coordinator Nodes**
- 在Druid擔任master角色，透過zookeeper管理Real-time和Historical Nodes，且透過MySQL管理segments的metadata
- Coordinator Nodes 指揮Historical Nodes去做load或drop segments，針對Historical Node做balance
5. **Overlord Nodes**
   - 管理Druid的索引任務，會將任務交給 MiddleManager，最後由Peon這個 worker去執行。
   
> Stream Pull 

如果Druid以Stream Pull的方式自動的從外部拉取資料而生成Indexing Service Tasks，我们则需要建立Real-Time Node
> Stream Push  

如果是採用Stream Push策略，需要建立一個"copy service"，負責從資料提供處取得資料並生成Indexing Service Tasks，從而將數據"推入"到Druid中(Tranquility)
## Indexing Service
indexing Service是負責"產生" Segment的高可用、分布式、Master/Slave架構 。主要由三類元素組成：
1. 負責運行索引任務(indexing task)的Peon
2. 負責控制Peon的MiddleManager
3. 負責任務分配给MiddleManager的Overlord
其中，Overlord和MiddleManager可以分散式部署，但是Peon和MiddleManager默認在同一台機器上。
## DataSchema
Timestamp column: queries center around the time axis, 此列會決定資料所在的Segment，系統中會儲存的column為__time
Dimension columns:  most commonly used in filtering the data
Metric columns: columns used in aggregations and computations
granularitySpec: 粒度設定，裡面的segmentGranularity參數即是設定，多久要進行一次segment

## Tranquility
取得Streaming data提交給Overload node去做Realtime的Index

Q: 加了zookeeper功能後，tranquility出現無法找到overlord node的錯誤訊息
- 需要在druid的config加上druid.host的參數，預設host是機器名稱，所以在zookeeper上無法找到對應的cluster node


## Ref
[Druid 系统框架](http://blog.csdn.net/gg782112163/article/details/59535679)


###### tags: `apache`, `druid`, `Tranquility`