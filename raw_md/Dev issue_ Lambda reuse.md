# Dev issue: Lambda reuse 

- 當系統透過 APIGateway 呼叫 Lambda 執行時，我以為Lambda會`全部`重新執行打包好的程式。所以開發時，我們將 database connection 物件當成 Global 物件使用，認為每次重新呼叫 Lambda 都會全部重新生成物件。因為這個觀念而導致系統錯誤，當 Project 的物件被 require 後或變成 global 參數，再次執行 Lambda container 會出現 reuse 特性，將不會再被重新執行而生成新物件，以下是一個範例。

> DB 的 client 為 global 物件
```javascript=
const pg = require('pg');

const client = new pg.Client('postgres://myrds:5432/dbname');  
client.connect();

exports.handler = (event, context, cb) => {  
  const {test_print} = require('./example_module');
  test_print();
  client.query('SELECT * FROM users WHERE ', (err, users) => {
    // Do stuff with users
    cb(null); // Finish the function cleanly
  });
};
```
- 上面的範例，因為 client 為 global物件，所以如果在程式裡面有 disconnect client 的狀況下，再次執行 Lambda 就會出現錯誤，因為 client 物件沒被重新 connect。

> Global 程式不會每次都被執行
```javascript=
console.log('init the test module.');

module.exports= {  
  function test_print(){
      console.log('test')
  }
};
```
在 handler 裏面如果去 require module，module一旦被載入後就會被保留 reuse 用途，所以執行第二次 'init the test module.' 字串就不會再出現。



- [Database Connections in Lambda](http://blog.rowanudell.com/database-connections-in-lambda/)
- [Understanding Container Reuse in AWS Lambda](https://aws.amazon.com/tw/blogs/compute/container-reuse-in-lambda/)


###### tags: `AWS`, `Lambda`, `reuse`,