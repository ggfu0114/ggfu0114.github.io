---
title: "Kubeflow安裝及入門"
description: "安裝Kubeflow系統在機器上，分享debug過程"
author: "GGFU"
date: "2020-12-31"
tags: 
---



### 安裝需求
- 安裝好ksonnet, Version 0.11.0 or later.
- Kubernetes 1.8 or later
#### 安裝ksonnet
```
export KS_VER=0.12.0
export KS_PKG=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_PKG}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_PKG}.tar.gz \
  --no-check-certificate
mkdir -p ${HOME}/bin
tar -xvf /tmp/$KS_PKG.tar.gz -C ${HOME}/bin
export PATH=$PATH:${HOME}/bin/$KS_PKG
```
官方皆學的網站可以參考：  [linux install ks](https://www.kubeflow.org/docs/guides/components/ksonnet/)

#### 安裝kubeflow
- 下載安裝kubeflow的script
```
export KUBEFLOW_SRC=kf_src
mkdir ${KUBEFLOW_SRC}
cd ${KUBEFLOW_SRC}
export KUBEFLOW_TAG=v0.3.1
curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash
```
- 將下載好的ks檔部署到K8S環境上
```
export KFAPP=kf_conf
scripts/kfctl.sh init ${KFAPP} --platform none
cd ${KFAPP}
../scripts/kfctl.sh generate k8s
../scripts/kfctl.sh apply k8s
```
#### 驗證kubeflow status
執行`kubectl get pods --all-namespaces`可以檢視目前pod運行的狀態
會發現有一個pod會是`pending`的狀態，`vizier-db-547967c899-ppr4p`
執行`kubectl describe vizier-db-547967c899-ppr4p -n kubeflow`
可以看到events出現以下字眼
```
Warning  FailedScheduling  1m (x67 over 6m)  default-scheduler  pod has unbound PersistentVolumeClaims
```
因為沒有PV，所以DB沒辦法正常啟動，所以只要建立一個PV給資料庫儲存東西就會解決這個問題。

#### Q:安裝過程出現`namespaces "kubeflow" not found`
- 因為Kubeflow version 0.3.0有點問題，只要改成0.3.1即可

#### Q:安裝啟動後pod出現以下的錯誤：
```
The node was low on resource: ephemeral-storage. Container statsd was using 52Ki, which exceeds its request of 0. Container ambassador was using 244Ki, which exceeds its request of 0. Container statsd-sink was using 52Ki, which exceeds its request of 0.
```
node的空間已經不夠了，導致我的pod被驅逐(evicted)


### 進入jupyter service
如果是在local端的主機自建的Kubeflow
有兩個方式可以進去到jupyter介面 
1. port forward 
```
kubectl port-forward svc/tf-hub-lb -n kubeflow 8080:80
```
在網頁上打入`http://127.0.0.1:8080`就可以看到網頁

2. node port

需要執行修改service`kubectl -n kubeflow edit svc tf-hub-lb`
修改成以下狀態
```
sessionAffinity: None
  type: NodePort
```

### 啟用GPU node
- 如果主機上有想要用GPU加速Machine Learning的速度，需要將有GPU的node加入Kubernates的cluster裡面
```
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.11/nvidia-device-plugin.yml
```
透過安裝nvidia plugin可以enable GPU的support
- 檢查node中gpu數量
```
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```


#### Q:
雖然在K8S環境上已經有join GPU的node, 但是還是無法取的GPU的資訊，用log看了一下gpu plugin pod的資訊，發現以下錯誤訊息：
```
2018/11/15 03:49:12 Failed to initialize NVML: could not load NVML library.
2018/11/15 03:49:12 If this is a GPU node, did you set the docker default runtime to `nvidia`?
```
解決的辦法為：修改`/etc/docker/daemon.json`的資訊，讓docker的default-runtime為nvidia
```
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

### 刪除kubeflow
kubectl delete namespace kubeflow -n kubeflow


### FAQ
執行ks init都會出現以下錯誤訊息：
`panic: runtime error: invalid memory address or nil pointer dereference`
上網查了一下好像是k8s版本為v1.12版本時所會出現的錯誤，必須降版到1.11去解決這個issue
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - && \
  echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list && \
  sudo apt-get update -q && \
  sudo apt-get install -qy --allow-downgrades kubelet=1.11.4-00 kubectl=1.11.4-00 kubeadm=1.11.4-00
```