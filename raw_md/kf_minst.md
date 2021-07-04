Title: Kubeflow Mnist範例介紹
Description: 利用簡單的mnist來做為範例，介紹如何在Kubeflow進行training跟serving的流程。Kubeflow利用argo workflow將整個流程寫成腳本，透過指令驅動整個AI training與serving過程
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/


# Kubeflow Mnist範例介紹

![](https://cdn-images-1.medium.com/max/1000/1*akWVsdGH6XW9SgDIiePq4Q.png)

官網的Git：[kubeflow mnist](https://github.com/kubeflow/example-seldon)
- 利用簡單的mnist來做為範例，介紹如何在Kubeflow進行training跟serving的流程。Kubeflow利用argo workflow將整個流程寫成腳本，透過指令驅動整個AI training與serving過程。training階段會將訓練model的程式碼包成docker image，建立TFjob將model訓練出來。serving階段，會將訓練好的model利用seldon-core的幫助，建立起prediction服務。

### Training 的流程
1. 將training的程式從git上載下來，打包成training image
2. 將打包好的image推上去docker registry
3. 利用TFjob執行image產生model
4. 將model給volume出來

### Serving 的流程
1. 將serving的程式從git上載下來，打包成serving image
2. 將打包好的image推上去docker registry
3. 將剛train好的model給volume到seldon-core的image上
4. 透過定義seldon graph啟動predict的機制

{%youtube ABislaVmNys %}

### 測試
可以利用**seldon-core**出的測試工具來檢視predict serving是否正確執行：
``` shell
$ seldon-core-api-tester --ambassador-path /seldon/kubeflow/mnist-classifier -p contract.json <host ip> <host port>
```

### Debug
> 錯誤訊息：
```
error when creating "/tmp/manifest.yaml": tfjobs.kubeflow.org is forbidden: User "system:serviceaccount:kubeflow:default" cannot create tfjobs.kubeflow.org in the namespace "kubeflow"
```
- 將kubeflow namespace的帳號default 加上cluster-admin的權限
```
kubectl create clusterrolebinding sa-admin --clusterrole=cluster-admin --serviceaccount=kubeflow:default
```

> 錯誤訊息：
```
 Failed to submit workflow: workflows.argoproj.io is forbidden: User "system:serviceaccount:kubeflow:jupyter-notebook" cannot create workflows.argoproj.io in the namespace "kubeflow"
```
因為jupyter的pod，serviceaccount預設為`jupyter-notebook`，綁定這個serviceaccount的role為`jupyter-notebook-role`，如果把`jupyter-notebook-role`資訊顯示出來看為
```
Name:         jupyter-notebook-role
Labels:       app.kubernetes.io/deploy-manager=ksonnet
              ksonnet.io/component=jupyterhub
Annotations:  ksonnet.io/managed={"pristine":"H4sIAAAAAAAA/4SQvU4rMRCF+/sYp4ycvUqH9gXoKWjQFuPdgTjr9VjjcSBEeXfkRQiJLdLZc873+ecKyuGZtQRJ6KGexo6qHUXDJ1mQ1M0PpQvy/3zwbHSAwxzShB5PEhkOCxtNZIT+ikieY2mruUhKbA0cZcmSOBl6nGq+...
PolicyRule:
  Resources               Non-Resource URLs  Resource Names  Verbs
  ---------               -----------------  --------------  -----
  deployments             []                 []              [*]
  pods                    []                 []              [*]
  replicasets             []                 []              [*]
  services                []                 []              [*]
  deployments.apps        []                 []              [*]
  replicasets.apps        []                 []              [*]
  jobs.batch              []                 []              [*]
  deployments.extensions  []                 []              [*]
  replicasets.extensions  []                 []              [*]
  *.kubeflow.org          []                 []              [*]
```
缺少了`workflows.argoproj.io`這個操作Argo的resource權限，所以我們可以透過編輯這個role來解決這個問題。在role的rule裡面加上：
```yaml
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  - workflows/finalizers
  verbs:
  - '*'
```


- 需要建立docker registery的帳號密碼。[docker-credentials-secret.yaml](https://github.com/kubeflow/example-seldon/blob/master/k8s_setup/docker-credentials-secret.yaml.tpl)
```
apiVersion: v1
data:
  password: <base 64 password>
  username: <base 64 username>
kind: Secret
metadata:
  name: docker-credentials
  namespace: default
type: Opaque
```
- 需要先建立nfs讓training放置訓練完的model。 [nfs.](https://github.com/kubeflow/example-seldon/blob/master/nfs.md)
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-1
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs-client
  resources:
    requests:
      storage: 30Gi
```
###### tags: `mnist` `seldon-core` `kubeflow` `argo` `tfjob` `model` `AI`