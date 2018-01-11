title: CI/CD Pipeline for Zappa-based Apps
timestamp: 2017-12-19 00:00:00
slug: ci-cd-for-zappa-based-apps
tags: [amazon-web-services, aws, code-pipeline, code-build, continuous-integration, continuous-deployment, devops]
author: Matt Healy

One of the most popular topics in technology over the last 12-18 months has been the concept of "Serverless" computing. I won't go in to to much detail about traditional cloud hosting vs serverless as there are plenty of resources out there concerning this. AWS provides a great serverless option called <a href="https://aws.amazon.com/lambda/">AWS Lambda</a>.

Some of the Python projects I've been working on at <a href="http://www.clientvault.com.au">ClientVault</a> recently have given me a great opportunity to try out AWS Lambda. We have a few products that are still at MVP or beta stage, so we didn't want to spend a lot of money running EC2 servers for such low usage. Serverless is a great option for scenarios like this - with such low usage you're unlikely to ever actually spend any money on Lambda.

Deploying any non-trivial Python application to AWS Lambda can be a bit tedious. Fortunately, excellent frameworks such as <a href="https://github.com/aws/chalice">Chalice</a>, <a href="https://serverless.com/">Serverless</a> and <a href="https://www.zappa.io/">Zappa</a> are out there to assist with this task. The one I chose was Zappa, as it seemed to be the most popular and the most regularly maintained. With Zappa, deploying to AWS Lambda for the first time is as simple as running `zappa init` followed by `zappa deploy`. Any subsequent updates are handled by a `zappa update`. What could be easier!?

This worked well for quite a while, but eventually I ran in to some problems
