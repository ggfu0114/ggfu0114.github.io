Title: PgPool2 install issu 紀錄安裝過程
Description: PgPool2 install issu 紀錄安裝過程
Authors: GGFU
Date: 03/06/2022
Tags: 
base_url: https://ggfu0114.github.io/

# PgPool2 install issu 紀錄安裝過程

## 安裝pgpool-II
透過網路上簡易的git repostory去快速的安裝pgpool-2 docker環境
例如：[docker-pgpool2](https://github.com/lzalewsk/docker-pgpool2)
1. 將pgpool conf檔跟執行的shell複製進去docker裡面
2. 執行pgpool

需要在postgres建立pgpool所需要登入的角色，例如使用者：pgpool

利用指令可以查詢現在postgres node status:
```
pcp_node_info [option...] [node_id]
pcp_node_info --verbose -h localhost -U postgres 0

```

### 問題

- 出現`2018-09-18 05:32:46: pid 6: FATAL:  could not open pid file as /var/run/pgpool/pgpool.pid. reason: No such file or directory`的錯誤訊息
需要幫process建立/var/run/pgpool的資料夾

- pgpool都已經裝好，postgres sever也已經就緒，但是出現無法登入的問題，相同帳號密碼不透過pgpool會登入成功？

- 看了一下pgpool2的log檔，出現以下資訊
```
2018-07-27 06:51:28 DEBUG: pid 30: I am 30 accept fd 5
2018-07-27 06:51:28 LOG:   pid 30: connection received: host=192.168.17.178 port=64325
2018-07-27 06:51:28 DEBUG: pid 30: Protocol Major: 1234 Minor: 5679 database:  user: 
2018-07-27 06:51:28 DEBUG: pid 30: SSLRequest from client
2018-07-27 06:51:28 DEBUG: pid 30: read_startup_packet: application_name: pgAdmin 4 - DB:postgres
2018-07-27 06:51:28 DEBUG: pid 30: Protocol Major: 3 Minor: 0 database: postgres user: postgres
2018-07-27 06:51:28 DEBUG: pid 30: new_connection: connecting 0 backend
2018-07-27 06:51:28 DEBUG: pid 30: new_connection: skipping slot 0 because backend_status = 0
2018-07-27 06:51:28 DEBUG: pid 30: new_connection: connecting 1 backend
2018-07-27 06:51:28 DEBUG: pid 30: pool_read_message_length: slot: 1 length: 12
2018-07-27 06:51:28 DEBUG: pid 30: pool_do_auth: auth kind:5
2018-07-27 06:51:28 DEBUG: pid 30: trying md5 authentication
2018-07-27 06:51:28 ERROR: pid 30: pool_get_passwd: username is NULL
2018-07-27 06:51:28 DEBUG: pid 30: do_md5: (null) does not exist in pool_passwd
2018-07-27 06:51:28 DEBUG: pid 30: do_md5failed in slot 1
```

- 正常普通安裝pgpool，設定檔的路徑會出現在`/etc/pgpool2`，通常會有四個檔案，`pcp.conf`  `pgpool.conf`  `pool_hba.conf`  `pool_passwd`

- 處理這個問題需要檢查幾個步驟：
1. `pgpool.conf`: 是否enable_pool_hba有開啟
```
# - Authentication -

enable_pool_hba = on
                                   # Use pool_hba.conf for client authentication
pool_passwd = 'pool_passwd'
                                   # File name of pool_passwd for md5 authentication.
                                   # "" disables pool_passwd.
                                   # (change requires restart)
authentication_timeout = 60
                                   # Delay in seconds to complete client authentication
                                   # 0 means no timeout.
```
2. `pool_hba.conf`: hba為host-based authentication的縮寫，這個檔案規範了哪些client可以存取哪些資料庫跟認證的方式，因為實驗關係，我將local全開，從外部連線進來的則需要透過md5驗證

 ```
 # TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD
 # "local" is for Unix domain socket connections only
local   all         all                               trust
# IPv4 local connections:
host    all         all         0.0.0.0/0               md5
 ```
3. `pool_passwd`: pgpool2是個中介角色，所以並不知道使用者的帳號密碼，所以需要在這邊建立可以存取pool的帳號密碼(當然帳號密碼要跟登入postgres的相同)

```
# FORMAT: "username:encrypted_passwd"
postgres:md56805f0aa765be4366313b21228496be1
```

md5後的密碼可以用兩種方式產生:
- `pg_md5 --md5auth --username=<username> <passowrd>`
密碼會自動地加入到pool_passwd檔案裡，或是到postres查詢
- `select * from pg_shadow;`


# Postgres HA
分別建立master與slave的postgres，然後執行slave作為master的replication的node時出現以下的錯誤
```
FATAL:database system identifier differs between the primary and standby
```
在slave的node，PG DATA需要由master的node複製過來才會有相同的identifier



在master-slave模式下將master關閉時，在slave log上會出現以下的錯誤訊息，slave會一直嘗試連線上去master，因為目前slave是沒有寫入的能力的
```
FATAL:  could not connect to the primary server: could not connect to server: Connection refused
                Is the server running on host "192.168.0.100" and accepting
                TCP/IP connections on port 5432?
```

使用pg_basebackup進行資料備份一直出現：
```no pg_hba.conf entry for replication connection from host "192.168.21.171", user "ubuntu", SSL off```
明明pg_hba.conf已經是，應該是所有連線只要有打密碼都可以連線上，但是情況是怎麼都會出現ERROR
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host all all all md5
```
原因：
需要在pg_hba加上以下這條rule，如果是replication connection，DATABASE的欄位一定是填replication。
`host    replication     replicator      all               md5`

# Pgpool2 HA
PGool透過watch dog開啟heartbeat模式互相偵測node彼此是否存活，搭配上Virtual IP去指定一個沒在使用的IP作為connect連接的入口，一旦active pgpool出現問題時，watchdog會請其他stanby的node建立Virtual IP的網路，取代原本active node.
### 開啟wd模式
[example-watchdog](http://www.pgpool.net/docs/latest/en/html/example-watchdog.html)
上面的連結有介紹了如何透過修改`pgpool.conf`去啟用watch dog功能
實驗過程出現以下錯誤：
```
SIOCSIFADDR: Operation not permitted 
SIOCSIFFLAGS: Operation not permitted 
SIOCSIFNETMASK: Operation not permitted 
```
因為pgpool是在docker container執行，所以沒有network變更權限，需要在run container時加上 -privileged

[簡中pgpool.conf說明](http://www.pgpool.net/docs/pgpool-II-3.2.1/pgpool-zh_cn.html)

###### tags: `postgres ha`, `pgpool`, `hba`, `replication`