# Serverless 佈署 lambda & API gateway -基礎篇
>說明
>
當使用 serverless package 佈署 AWS resources，serverless 會在專案的檔案夾內建立一個名為`.serverless`的檔案夾，裡面會存有 `cloudformation-template-create-stack.json`, `cloudformation-template-update-stack.json`, `{project}.zip`三隻檔案。

`cloudformation-template-create-stack.json`: 會在S3創立一個bucket儲存專案程式碼的空間
`cloudformation-template-update-stack.json`: 佈署專案所需要的所有資源
- cloudformation:DescribeStacks
- cloudformation:DescribeStackResources
- cloudformation:UpdateStack
- cloudformation:ListStacks
- iam:GetRole
- lambda:UpdateFunctionCode
- lambda:UpdateFunctionConfig
- lambda:GetFunctionConfiguration
- lambda:AddPermission
- s3:DeleteObject
- s3:GetObject
- s3:ListBucket
- s3:PutObject
:::danger
##### 執行serverless deploy時會出現cloudformation權限問題

![](https://i.imgur.com/3c8ai4Q.png)

:a: 需要到IAM上幫user加上AdministrateAccess的權限，serverless才可以在cloudformation上面幫忙佈署lambda的function。畫面如同下方

![](https://i.imgur.com/QGdLGfD.png)
:::

