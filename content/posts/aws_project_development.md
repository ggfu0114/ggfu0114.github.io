---
title: "在Local machine開發AWS serverless project"
description: "這個 Project 主要是拿來研究 AWS serverless 的開發規劃和未來建構 Project 的基礎參考。主要會用到 AWS Resource 有 API-gateway, Lambda, RDS, Congnito Services。"
author: "GGFU"
date: "2020-12-31"
tags: 
- AWS
---



# AWS dev project
- 說明：這個 Project 主要是拿來研究 AWS serverless 的開發規劃和未來建構 Project 的基礎參考。主要會用到 AWS Resource 有 API-gateway, Lambda, RDS, Congnito Services。

# Install
- 安裝 serverless package
`npm install -g serverless`
- 安裝開發所需其他的套件
`npm install`


# Dev run
- Project 開發時，可在本機上做 Debug，確定Lambda的function沒有邏輯錯誤再佈署上去AWS就可以。Dev server開啟時會建立在 port 3000 上，請用自己主機 ip 連，不要用 <font color=red>127.0.0.1</font> 或 <font color=red>localhost</font> 連線，否則會出現錯誤。
`npm run dev`

# Deploy to AWS
- 將自己的程式碼透過serverless package上傳到 CloudFormation後佈署所需資源。
`npm run deploy`
- 為 API-gateway建立一個 Usage Plan
`aws apigateway create-usage-plan --name dev-file-sharing-plan --api-stages apiId={{API_ID}},stage=dev --region ap-northeast-1`
- 為 Usage Plan 綁定一組 API-key
`aws apigateway create-usage-plan-key --usage-plan-id {{PLAN_ID}} --key-id {{KEY_ID}} --key-type "API_KEY"`

# Migrations
- 建立一個 Migration 檔案 (若變更 Schema 則需要新增一個 Migration 檔案)
- `db-migrate create <migrate_file> --config ../config.json`
- 執行 migrate
- `db-migrate up --config ../config.json -e dev -v`
- `db-migrate up --config ../config.json -e prod -v`
- 回復最原始的 migration (execute all down migrations and literally reset all migrations)
- `db-migrate reset ../config.json -e prod -v`
:smile: 目前自動化 Delpoy 還有研究空間

