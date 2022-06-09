---
title: "Kubernate Env Setup FAQ(by Kubeadm)"
description: "Kubernate Env Setup FAQ(by Kubeadm)"
author: "GGFU"
date: "2022-03-06"
tags: 
---

### 前置作業
如何關掉swap功能：
如果是linux，可透過以下指令去關掉swap功能
`sudo swapoff -a && sudo sed -i '/swap/d' /etc/fstab`

### 安裝執行工具
安裝kubelet kubeadm kubectl的方法
```
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
官網說明：https://kubernetes.io/docs/setup/independent/install-kubeadm/


### 開始架設
將電腦變成master node可執行：
```
kubeadm init
```
首先adm會先去做幾項檢測
通過後會下載跟安裝k8s所需要的控制元件



### 安裝過程的錯誤
#### Q1
```
Unable to connect to the server: x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "kubernetes")
```
主要是因為沒執行以下的動作，導致user的權限不符合，無法使用kubctl cmd

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```



#### Q2
```
runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
```
kubectl logs -f <pod id> -n kube-system
```
failed to acquire lease: node "ubuntu" pod cidr not assigned
```

執行`kubectl get pods --all-namespaces`會發現coreDns會是pending status
需要先安裝flannel套件，並重啟kubeadm init加上`kubeadm init --pod-network-cidr=10.244.0.0/16`
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
也可安裝WeaveNet：
```
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```
#### Q3
執行`kubectl get pods --all-namespaces`，裝完flannel出現以下錯誤
```
kube-system   coredns-576cbf47c7-hnnt2       0/1     CrashLoopBackOff   1          11m
```
利用kubectl logs -f coredns-576cbf47c7-hnnt2  -n kube-system，看到以下錯誤的error message.
```
2018/09/22 07:39:38 [FATAL] plugin/loop: Seen "HINFO IN 8205794187887631643.5216586587165434789." more than twice, loop detected
```

上網找了一些資料，發現了以下這篇
https://blog.csdn.net/crystonesc/article/details/83387659
主要原因: coredns會直接取用本機上/etc/resolv.conf裡的nameserver參數作為upstream server，在ubuntu系統上/etc/resolv.conf會加入自己的ip當作nameserver，所以導致無限循環，所以在log裡會見到loop detected

修改coredns configmap檔可以解決這個問題。
執行以下CMD來修改configmap參數
`kubectl edit cm coredns -n kube-system` 
將`/etc/resolv.conf`取代為`8.8.8.8`

#### Q4
將server給裝起來時describe出現以下錯誤訊息
`Liveness probe failed`,`Readiness probe failed`
代表server的pod沒有正確提供kubectl一個良好監控管道去得知pod的狀態
```
livenessProbe:
httpGet:
  path: /liveliness
  port: http
readinessProbe:
httpGet:
  path: /readiness
  port: http
```
例如上面的設定檔代表kubectl會利用http偵測`/liveliness`,`/readiness`去得知有沒有response來決定pod是否存活與就緒

#### Q5 what are flannel and cni
- [flannel](https://feisky.gitbooks.io/sdn/container/flannel/)
- [cni](https://feisky.gitbooks.io/sdn/container/cni/)