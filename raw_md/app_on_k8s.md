Title: 部屬Web application到K8S環境
Description: 在K8S的環境中,設定Application的網路環境, 讓使用者可以存取到資源。
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/

# Deploy first API server on K8S

## prepare server image
docker pu
image to registery

## deploy pod on K8S


執行create pod指令時出現以下錯誤，代表目前K8S架構裡只有Master沒有Node
```
0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate
```
執行 `kubectl get pods -o wide` 可以檢查目前pod的運行狀態
```
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE     NOMINATED NODE
my-pod   1/1     Running   0          19m   10.244.1.2   ubuntu   <none>
```
- 驗證server是否已經成功的運行，可以用建立另一個暫時的pod，利用curl指令去取得server的資訊

```
kubectl run -i --tty alpine --image=alpine --restart=Never -- sh
apk add curl
curl -v http://10.244.1.2
```

## service expose 


#### NodePort
建立NodePort service開放port在node上，讓外部可以存取到Kubernetes Cluster內的Pod.
執行`kubectl get svc`取得目前service的列表如下：
```
django-service   NodePort    10.97.136.223   <none>        80:30390/TCP   7m31s
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP        21h
```
以上的狀態目前有一個service IP為10.97.136.223，他會將30390收集到的資料導倒80port，
所以現在只要在node上執行`curl -v http://<nodeip>:30390`就可以取得django server的回應

#### Ingress
因為NodePort有一些限制和缺點
- port只能介於30000–32767
- 一個port只能接一個service
- node IP變動的話系統就需要修改參數

所以Ingress就被創立出來解決這些事情。
首先在K8S環境中創立Ingress Controller
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml`
執行
`kubectl get pods --all-namespaces -l app.kubernetes.io/name=ingress-nginx --watch`
可以去驗證Ingress Controller是否成功被建立出來。





## join nodes to K8S
- get token on master node，產出<token id>
```
kubeadm token list
```
- generate token ca-cert，產出<ca-cert>
```
sudo openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```
- run cmd on node
```
sudo kubeadm join --token <token id> <master ip>:6443 --discovery-token-ca-cert-hash sha256:<ca-cert>
```

OR

```
sudo kubeadm token create --print-join-command
```

#### Q:在Join nodes時pods會有pending現象，describe pod狀態後都會發現以下錯誤
```
failed to set bridge addr: "cni0" already has an IP address different from 10.244.3.1/24
```
解決辦法為：
```
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
```