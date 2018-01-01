title: CI/CD Pipeline for Zappa-based Apps
timestamp: 2017-12-19 00:00:00
slug: ci-cd-for-zappa-based-apps
tags: [amazon-web-services, aws, code-pipeline, code-build, continuous-integration, continuous-deployment, devops]
author: Matt Healy

One of the most popular topics in technology over the last 12-18 months has been the concept of "Serverless" computing. I won't go in to to much detail about traditional cloud hosting vs serverless as there are plenty of resources out there concerning this. AWS provides a great serverless option called <a href="https://aws.amazon.com/lambda/">AWS Lambda</a>. 
Deploying any non-trivial Python application to AWS Lambda can be a bit tedious. Fortunately, excellent frameworks such as <a href="https://github.com/aws/chalice">Chalice</a>, <a href="https://serverless.com/">Serverless</a> and <a href="https://www.zappa.io/">Zappa</a> are out there to assist with this task. 

