#!/bin/bash
cd app/build && aws s3 sync ./ s3://your-bucket-here/ --acl public-read
aws cloudfront create-invalidation --distribution-id your-distribution-id-here --paths '/*'
