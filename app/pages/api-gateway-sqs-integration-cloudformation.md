title: API Gateway Integration with SQS via CloudFormation
timestamp: 2019-05-26 00:00:00
slug: api-gateway-sqs-integration-cloudformation
tags: [cloudformation, aws, apigateway, sqs]
author: Matt Healy

A neat feature of Amazon Web Service's <a href="https://aws.amazon.com/api-gateway/">API Gateway</a> service is that it can integrate directly with other AWS services. The most common use of API Gateway is to integrate directly with a <a href="https://aws.amazon.com/lambda/">Lambda</a> function, typically to perform an action like update a DynamoDB table or send a message to an SQS queue. But, sometimes it is not actually necessary to use a Lambda function at all - by taking advantage of API Gateway's AWS service integration, we can avoid this intermediary step altogether and build a much more efficient and resilient architecture.

I recently had a need to provision a simple API endpoint that would accept a JSON payload and store the data to be processed later. Typically I would look to use API Gateway backed by a basic Lambda function to accept the JSON data and store it in an SQS queue. Instead, for this project I opted to use the API Gateway AWS service integration with the SQS queue.

By using the AWS service integration, we benefit in a number of ways:

1. There is no code to write or maintain
2. Reduced latency - with no Lambda function to start (potentially from a cold start) we can receive a response from the API Gateway much quicker
3. We don't eat in to our allocated Lambda invocation limits. By default, we only have 1,000 concurrent executions allowed across all functions. When we use the AWS service integration this limit doesn't concern us.

There are a number of <a href="https://dzone.com/articles/creating-aws-service-proxy-for-amazon-sqs">blog</a> <a href="https://medium.com/@pranaysankpal/aws-api-gateway-proxy-for-sqs-simple-queue-service-5b08fe18ce50">posts</a> that do an excellent job of describing how to set up this API Gateway to SQS architecture, but none that explain how to do the same using <a href="https://aws.amazon.com/cloudformation/">CloudFormation</a>, Amazon's "Infrastructure as Code" solution.

After a bit of trial and error, I managed to come up with the below Cloudformation template which does the following:

1. Creates an SQS queue with the name based on the parameter supplied
2. Assigns a queue policy allowing messages to be sent to the queue
3. Creates an IAM Role with permissions to allow API Gateway to send messages to SQS
4. Creates a REST API endpoint with POST method, configured with the SQS integration

Please feel free to use the below template or modify it to suit your own needs.
<hr />

<a href="https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apigatewaysqs&templateURL=https://cf-templates-1ljknwz295obo-ap-southeast-2.s3.amazonaws.com/api-gateway-sqs-integration-20190526.yaml">
    <img src="/static/img/blog/cloudformation-launch-stack.png" />
</a>
<a class="btn btn-default" href="https://cf-templates-1ljknwz295obo-ap-southeast-2.s3.amazonaws.com/api-gateway-sqs-integration-20190526.yaml"><i class="fa fa-download" aria-hidden="true"></i> Download Template</a>

    Description: API Gateway integration with SQS
    Outputs:
      ApiEndpoint:
        Description: Endpoint for this stage of the api
        Value: !Join
          - ''
          - - https://
            - !Ref 'APIGateway'
            - .execute-api.
            - !Ref 'AWS::Region'
            - .amazonaws.com/
            - prod
      QueueArnSQS:
        Description: ARN of SQS Queue
        Value: !GetAtt 'DestQueue.Arn'
    Parameters:
      queueName:
        Description: The name of the SQS queue to create.
        Type: String
    Resources:
      APIGateway:
        Properties:
          Description: API Endpoint to receive JSON payloads and queue in SQS
          Name: APIGateway
        Type: AWS::ApiGateway::RestApi
      APIGatewayRole:
        Properties:
          AssumeRolePolicyDocument:
            Statement:
              - Action:
                  - sts:AssumeRole
                Effect: Allow
                Principal:
                  Service:
                    - apigateway.amazonaws.com
            Version: '2012-10-17'
          Path: /
          Policies:
            - PolicyDocument:
                Statement:
                  - Action: sqs:SendMessage
                    Effect: Allow
                    Resource: !GetAtt 'DestQueue.Arn'
                  - Action:
                      - logs:CreateLogGroup
                      - logs:CreateLogStream
                      - logs:PutLogEvents
                    Effect: Allow
                    Resource: '*'
                Version: '2012-10-17'
              PolicyName: apig-sqs-send-msg-policy
          RoleName: apig-sqs-send-msg-role
        Type: AWS::IAM::Role
      DestQueue:
        Properties:
          DelaySeconds: 0
          MaximumMessageSize: 262144
          MessageRetentionPeriod: 1209600
          QueueName: !Ref 'queueName'
          ReceiveMessageWaitTimeSeconds: 0
          VisibilityTimeout: 30
        Type: AWS::SQS::Queue
      PolicySQS:
        Properties:
          PolicyDocument:
            Statement:
              - Action: SQS:*
                Effect: Allow
                Principal: '*'
                Resource: !GetAtt 'DestQueue.Arn'
                Sid: Sid1517269801413
            Version: '2012-10-17'
          Queues:
            - !Ref 'DestQueue'
        Type: AWS::SQS::QueuePolicy
      PostMethod:
        Properties:
          AuthorizationType: NONE
          HttpMethod: POST
          Integration:
            Credentials: !GetAtt 'APIGatewayRole.Arn'
            IntegrationHttpMethod: POST
            IntegrationResponses:
              - StatusCode: '200'
            PassthroughBehavior: NEVER
            RequestParameters:
              integration.request.header.Content-Type: '''application/x-www-form-urlencoded'''
            RequestTemplates:
              application/json: Action=SendMessage&MessageBody=$input.body
            Type: AWS
            Uri: !Join
              - ''
              - - 'arn:aws:apigateway:'
                - !Ref 'AWS::Region'
                - :sqs:path/
                - !Ref 'AWS::AccountId'
                - /
                - !Ref 'queueName'
          MethodResponses:
            - ResponseModels:
                application/json: Empty
              StatusCode: '200'
          ResourceId: !Ref 'enqueueResource'
          RestApiId: !Ref 'APIGateway'
        Type: AWS::ApiGateway::Method
      enqueueResource:
        Properties:
          ParentId: !Ref 'v1Resource'
          PathPart: enqueue
          RestApiId: !Ref 'APIGateway'
        Type: AWS::ApiGateway::Resource
      prodDeployment:
        DependsOn: PostMethod
        Properties:
          RestApiId: !Ref 'APIGateway'
        Type: AWS::ApiGateway::Deployment
      prodStage:
        Properties:
          DeploymentId: !Ref 'prodDeployment'
          RestApiId: !Ref 'APIGateway'
          StageName: prod
        Type: AWS::ApiGateway::Stage
      v1Resource:
        Properties:
          ParentId: !GetAtt 'APIGateway.RootResourceId'
          PathPart: v1
          RestApiId: !Ref 'APIGateway'
        Type: AWS::ApiGateway::Resource
