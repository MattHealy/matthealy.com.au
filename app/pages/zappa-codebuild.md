title: CI/CD Pipeline for Zappa-based Apps
timestamp: 2017-12-19 00:00:00
slug: ci-cd-for-zappa-based-apps
tags: [amazon-web-services, aws, code-pipeline, code-build, continuous-integration, continuous-deployment, devops]
author: Matt Healy

One of the most popular topics in technology over the last 12-18 months has been the concept of "Serverless" computing. I won't go in to to much detail about traditional cloud hosting vs serverless as there are plenty of resources out there concerning this. AWS provides a great serverless option called <a href="https://aws.amazon.com/lambda/">AWS Lambda</a>.

Some of the Python projects I've been working on at <a href="http://www.clientvault.com.au">ClientVault</a> recently have given me a great opportunity to try out AWS Lambda. We have a few products that are still at MVP or beta stage, so we didn't want to spend a lot of money running EC2 servers for such low usage. Serverless is a great option for scenarios like this - with such low usage you're unlikely to ever actually spend any money on Lambda.

Deploying any non-trivial Python application to AWS Lambda can be a bit tedious. Fortunately, excellent frameworks such as <a href="https://github.com/aws/chalice">Chalice</a>, <a href="https://serverless.com/">Serverless</a> and <a href="https://www.zappa.io/">Zappa</a> are out there to assist with this task. The one I chose was Zappa, as it seemed to be the most popular and the most regularly maintained. With Zappa, deploying to AWS Lambda for the first time is as simple as running `zappa init` followed by `zappa deploy`. Any subsequent updates are handled by a `zappa update`. What could be easier!?

This worked well for quite a while, but eventually I ran in to some problems.

1. `zappa update` works by downloading packages locally, creating a zip archive of your application with its dependencies, uploading that archive to S3 and then deploying the function code to Lambda. We have a really poor internet connection at the office, and this project archive can typically be around 20MB in size. That file can take several minutes to upload to S3 from our office, and chokes the connection for everyone else while it's uploading.

2. It feels a bit "ad hoc" to deploy an application (potentially mission-critical) based off a configuration on my development machine. Also, if anyone else in the organisation wants to deploy an update, it means they have to have the correct development environment set up on their machine. There's just too much room for error here.

The solution to problem (1) is to use a build service. Being "all-in" on AWS, it made sense for us to go with an AWS solution - CodeBuild. For those unfamiliar with a build service, it basically does what it says on the tin. Your code is uploaded to the service, a build is run according to instructions you provide, and the resulting build is sent somewhere. We ideally want the build to be triggered as soon as the code is updated. For this, we create a pipeline using AWS CodePipeline. Step one in the pipeline is the "master" branch of our git repository being updated. Step two is the CodeBuild project running a "zappa update" on the project source, thereby building and deploying the project to Lambda.
