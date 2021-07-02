# AWS IoT with websocket

- 在大多數的瀏覽器都有支援websocket的protocol前提下，實作網頁即時接收訊息的功能上，我們希望每個網頁都可以當作是一個mqtt的裝置，如此一來就可以即時推播給各個網頁，也可以即時的接收到來自client端的訊息。
- AWS在IoT的服務上也有做到MQTT Over the WebSocket Protocol，透過AWS SigV4的身份認證, 利用Port 443，我們可以透過網頁連線上AWS IoT的服務。

> server side
- 以下是server端需要產出帶有authentication的query url，使用上，前端只需要將url用get的方式呼叫就可以連接上IoT。
```javascript=
function SigV4Utils() {}

SigV4Utils.getSignatureKey = function (key, date, region, service) {
    var kDate = AWS.util.crypto.hmac('AWS4' + key, date, 'buffer');
    var kRegion = AWS.util.crypto.hmac(kDate, region, 'buffer');
    var kService = AWS.util.crypto.hmac(kRegion, service, 'buffer');
    var kCredentials = AWS.util.crypto.hmac(kService, 'aws4_request', 'buffer');    
    return kCredentials;
};

SigV4Utils.getSignedUrl = function(host, region, 
                                   ) {
    var datetime = AWS.util.date.iso8601(new Date()).replace(/[:\-]|\.\d{3}/g, '');
    var date = datetime.substr(0, 8);

    var method = 'GET';
    var protocol = 'wss';
    var uri = '/mqtt';
    var service = 'iotdevicegateway';
    var algorithm = 'AWS4-HMAC-SHA256';

    var credentialScope = date + '/' + region + '/' + service + '/' + 'aws4_request';
    var canonicalQuerystring = 'X-Amz-Algorithm=' + algorithm;
    canonicalQuerystring += '&X-Amz-Credential=' + encodeURIComponent(credentials.accessKeyId + '/' + credentialScope);
    canonicalQuerystring += '&X-Amz-Date=' + datetime;
    canonicalQuerystring += '&X-Amz-SignedHeaders=host';

    var canonicalHeaders = 'host:' + host + '\n';
    var payloadHash = AWS.util.crypto.sha256('', 'hex')
    var canonicalRequest = method + '\n' + uri + '\n' + canonicalQuerystring + '\n' + canonicalHeaders + '\nhost\n' + payloadHash;

    var stringToSign = algorithm + '\n' + datetime + '\n' + credentialScope + '\n' + AWS.util.crypto.sha256(canonicalRequest, 'hex');
    var signingKey = SigV4Utils.getSignatureKey(credentials.secretAccessKey, date, region, service);
    var signature = AWS.util.crypto.hmac(signingKey, stringToSign, 'hex');

    canonicalQuerystring += '&X-Amz-Signature=' + signature;
    if (credentials.sessionToken) {
        canonicalQuerystring += '&X-Amz-Security-Token=' + encodeURIComponent(credentials.sessionToken);
    }

    var requestUrl = protocol + '://' + host + uri + '?' + canonicalQuerystring;
    return requestUrl;
};

```
- `host`: IoT的endpoint, 例如：ag35axgb1wdct.iot.ap-northeast-1.amazonaws.com
- `region`: IoT service所在區域，例如：ap-northeast-1
- `credentials`: accessKeyId, secretAccessKey, sessionToken(optional) IAM角色的公私鑰

> client side
- 前端只要利用API的方式去向server取的IoT url並取代掉`{URL_FROM_SERVER}`就可以進行連線。修改連線的topic只需要取代掉`Test/chat`即可。
```htmlmixed=
<!DOCTYPE html>
<html lang="EN">

<head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
    <meta content="utf-8" http-equiv="encoding">
</head>

<body>
    <ul id="chat">
        <li v-for="m in messages">{{ m }}</li>
    </ul>
    <input type="text" name="say" id="say" placeholder="Input a message here...">
    <button id="send">Send</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.16/vue.min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/components/core-min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/components/hmac-min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/components/sha256-min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <script type="text/javascript">
        var data = {
            messages: []
        };
        new Vue({
            el: '#chat',
            data: data
        });
        document.getElementById('send').addEventListener('click', function (e) {
            var say = document.getElementById('say')
            send(say.value);
            say.value = '';
        });
var clientId = Math.random().toString(36).substring(7);
        var client = new Paho.MQTT.Client({URL_FROM_SERVER}, clientId);
        var topicName = 'Test/chat';
        var connectOptions = {
            useSSL: true,
            timeout: 3,
            mqttVersion: 4,
            onSuccess: subscribe
        };
        client.connect(connectOptions);
        client.onMessageArrived = onMessage;
        client.onConnectionLost = function (e) { console.log(e) };
        function subscribe() {
            client.subscribe(topicName);
            console.log("subscribed on Topic", topicName);
        }
        function send(content) {
            var message = new Paho.MQTT.Message(content);
            message.destinationName = topicName;
            client.send(message);
            console.log("sent to Topic", topicName);
        }
        function onMessage(message) {
            data.messages.push(message.payloadString);
            console.log("message received: " + message.payloadString);
        }
    </script>
</body>

</html>
```


###### tags: `AWS`, `IoT`, `websocket`, `SigV4`