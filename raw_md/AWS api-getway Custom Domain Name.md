# AWS api-getway Custom Domain Name

利用AWS的serverless服務開發 httpserver的情況下，很常會使用(Lambda+Apigateway)的服務，通常會用api-getway去當url route的服務。部屬成功時，api-getway都會給一組類似以下的網址，https://${api-id}.execute-api.region.amazonaws.com/stage ，因為網址有可能因為部署的需求而改變，所以如果想要制定自己的url名稱，就得使用api-getway裡面的custom domain name功能。

設定custom domain name分成以下幾個主要步驟
1. 申請AWS ACM(AWS Certificate Manager)服務
2. 綁定ACM服務到api-gateway
3. 將route53綁定到api-gateway產出的CDN網址

> 申請AWS ACM

如果要使用custom domain name，我們得提供有效的SSL/TLS certificate保護我們的網址。ACM是AWS專門管理或產出SSL/TLS憑證的服務，需要在上面申請保護我們的url，請注意!!! 如果是因custom domain name而需申請ACM的話，請將申請區域調到 ==US East (N. Virginia)==
。[ACM](http://docs.aws.amazon.com/acm/latest/userguide/)
- 申請的畫面會如下圖，如果想保護所有subdoamin可以用wildcard寫法，使用*號，例如：*.example.com
![](https://i.imgur.com/Kn8PBj3.png)
- 申請結束後AWS會寄信給domain擁有人(基本上就是開發者)，要求是否同意授權保護此網址，只要點擊連結就會啟用服務。
![](https://i.imgur.com/cCFELkO.png)

> api-gateway綁定ACM
- 申請好ACM就可以將custom domain name綁定到api-getway上。填好要綁定的domain名稱，剛創建好的ACM服務，與選定mapping的api-getway即可。綁定的過程中會出現 `Target Domain Name` 這個就要最後一步要將route53指向的cloud front網址。

![](https://i.imgur.com/J7pznKF.png)

> route53 綁定 cdn
- 登入進 route 53，為自己的domain建立一個A record，將target指向剛剛所產生的cloud front網址。
![](https://i.imgur.com/YbfKlFP.png)

以上步驟都完成時就可以使用自己所設定的domain name去存取server了。
###### tags: `apigetway`, `domain name`, `custom`, `route53`, `ACM`