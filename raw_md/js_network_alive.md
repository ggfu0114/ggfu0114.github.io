Title: Javascript detect network connect status
Description: 當我們在開發網站時，可能會遇到需要偵測網路情況，給予使用者是當的反饋。例如做檔案上傳時，如果網路斷線又回復連接時，需要提醒使用者可以做續傳的動作
Authors: GGFU
Date: 31/12/2020
Tags: 
base_url: https://ggfu0114.github.io/


# [JS] detect network connect status
- 當我們在開發網站時，可能會遇到需要偵測網路情況，給予使用者是當的反饋。例如做檔案上傳時，如果網路斷線又回復連接時，需要提醒使用者可以做續傳的動作。目前市面上多樣的瀏覽器所提供的`online`/`offline`事件，可能沒有辦法有效的偵測到。

:::warning
It is important to note that this event and attribute are inherently unreliable. A computer can be connected to a network without having Internet access.
:::

- 目前各家瀏覽器針對 "Offline" 的定義都不相同，所以沒有一個有效率的方式可偵測瀏覽器的網路情況。斷線的定義位於broswer當電腦在受保護的私人網路下，所以沒有連線到外界網路的能力，要定義為Offline嗎？ 都沒接上網路但是client和server端都在127.0.0.1網段，可以互相溝通要算有網路嗎？

一般開發網站時可能比較需要偵測連線到外埠網路的情況，所以下面是一斷偵測網路連線狀態的 example code。藉由嘗試存取自己網站的favicon.ico去判定對是否有網路的連線能力，我們透過 httprequest 的 HEADER method 去嘗試，再這個 method 下比較節省流量。[HTTP Method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
:::warning
The HEAD method asks for a response identical to that of a GET request, but without the response body
:::

```javascript
export function doesConnectionExist() {
    return new Promise((resolve) => {
        const xhr = new XMLHttpRequest();
        const url = 'https://example.com/favicon.ico';
        const randomNum = Math.round(Math.random() * 10000);
        function processRequest() {
            if (xhr.readyState === 4) {
                if (xhr.status !== 0) {
                    resolve({ net: 'connect', time: new Date() });
                } else {
                    resolve({ net: 'disconnect', time: new Date() });
                }
            }
        }

        xhr.timeout = 2000;
        xhr.open('HEAD', `${url}?rand=${randomNum}`, true);
        xhr.send();
        xhr.addEventListener('readystatechange', processRequest, false);
    });
}
```


###### tags: `Javascript`, `httprequest`, `network`, `online`, `offline`