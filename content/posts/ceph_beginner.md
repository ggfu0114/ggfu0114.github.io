---
title: "Ceph Cluster Storage 初階學習"
description: "學習Ceph storage的基本資訊與如何安裝系統"
author: "GGFU"
date: "2020-12-31"
tags: 
- Ceph
- CRUSH
- straw
---


# Ceph Cluster Storage 初階學習
## Ceph 元件
1. MON (monitor):
   - 維護整個cluster的狀態
   - 透過crush演算法取得osd位置，執行建立與傳輸資料
   - 不會主動的輪詢OSD的各種狀態
   - 保證cluster所有數據的一致性
	- 單一可運行，建議可部署多個，每個node上最多只能有一個MON
2. OSD (ObjectStorageDevice)
	- cluster中的資料的儲存體
   	- 當OSD發現自身或其他OSD發生異常時會上報MON
   	- 對其他的OSD發送heart beat訊號
3. MGR
4. MDS
	- 使用CephFS才需要使用此服務
   	- 提供資料運算，緩存和資料同步

Ceph RGW(即RADOS Gateway)是Ceph对象存储网关服务，是基于LIBRADOS接口封装实现的FastCGI服务，对外提供存储和管理对象数据的Restful API。
![](ceph-rgw.png)

安裝osd時有錯誤發生，發現log的描述如下：
** ERROR: osd init failed: (36) File name too long
原因：
Ceph官方建議用XFS作OSD的文件系統，如果安裝OSD主機上的文件系統格式為ext4，會使得OSD的資料不能安全的保存。所以要解決這個問題就得：
1. 將安裝OSD的文件系統改為XFS
2. 修改OSD的文件配置，然後重新啟動OSD
```
osd max object name len = 256 
osd max object namespace len = 64 
```

用來檢查Ceph目前的狀態
```
ceph -s

```

當Ceph系統都已經架設完畢時，可以安裝ceph-fuse作為Client端掛載到monitor機器上
sudo apt-get install ceph-fuse
```
$ ceph- fuse -m 192.168.0.1:6789 /fuse_folder/
```
系統都已設定完畢，但是使用ceph-fuse出現
```
mount failed: (110) Connection timed out
```

安裝Ceph的作業系統為`Ubuntu (14.04.4 LTS, Trusty Tahr)`
使用-d去debug時，會出現以下訊號
```
2018-03-13 10:20:03.234048 7f90c64cf700  0 -- 192.168.100.65:0/2082429148 >> 192.168.100.65:6789/0 pipe(0x55e333394b00 sd=0 :58114 s=1 pgs=0 cs=0 l=1 c=0x55e333394d90).connect protocol feature mismatch, my 2fffffffffff < peer 10ff8eea4fffb missing 401000000000000
```
主要的原因是CRUSH演算法的問題：
missing 401000000000000 = CEPH_FEATURE_CRUSH_V4(1000000000000)+CEPH_FEATURE_NEW_OSDOPREPLY_ENCODING(400000000000000)
CRUSH 的演算法用來計算資料的儲存位置，用來確定儲存與檢索。CRUSH授予client端可以存取OSD，避免單點故障，性能的限制，與系統擴展的限制。CRUSH裡面有一張Map，可以把資料平均隨機的散布到各個OSD裡。

當前內核的版本缺乏 CEPH_FEATURE_CRUSH_V4 這個特性，查表 > [feature set mismatch]('http://cephnotes.ksperis.com/blog/2014/01/21/feature-set-mismatch-error-on-ceph-kernel-client/')

解決辦法：修改crushmap，將straw2改成straw
```
$ ceph osd crush show-tunables #查訊目前tunables的參數
$ ceph osd crush tunables hammer #調整tunables至hammer
$ ceph osd crush dump|grep alg #查詢當前的crush演算法
#修改crush map 里面的bucket的alg
$ ceph osd getcrushmap -o crushmap.txt
$ crushtool -d crushmap.txt -o crushmap-decompile
$ vim crushmap-decompile
$ crushtool -c crushmap-decompile  -o crushmap-compile
$ ceph osd setcrushmap -i crushmap-compile
```

## Ceph plugin
- dashboard
  在 Luminous August 2017以後的 Development 版本，都有提供dashboard的功能，可以用網頁的方式去監控 Ceph的 狀態，安裝好Ceph的系統後，只需要enable模組即可。
```
ceph mgr module enable dashboard
```
預設的網頁server會綁定在：
如果有需要更改IP或PORT可以用以下方去做調整
```
ceph config-key set mgr/dashboard/server_addr $IP
ceph config-key set mgr/dashboard/server_port $PORT
```
[Ceph Dashboard 官網]('http://docs.ceph.com/docs/master/mgr/dashboard/')

