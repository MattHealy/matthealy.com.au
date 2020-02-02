title: Listing all CodeCommit Pull Requests
timestamp: 2020-02-02 00:00:00
slug: listing-all-codecommit-pull-requests
tags: [python, aws, codecommit, git]
author: Matt Healy

<a href="https://aws.amazon.com/codecommit/">AWS CodeCommit</a> is Amazon Web Service's Git hosting service and part of their suite of developer tools. It can be thought of as a comparable service to something like <a href="https://github.com/">GitHub</a> or <a href="https://about.gitlab.com/">GitLab</a> although being completely honest both of those services are ahead of CodeCommit in terms of usability and feature set. It does however have the advantage of being closely tied to other AWS services, in particular IAM for permission management.

CodeCommit allows for the usual development workflow of Pull Requests. However, something annoying about this is that you can only view outstanding pull requests against a sigle repository. There is no way in the AWS Console to have an overview of all outstanding pull requests across all code repositories in your account (within the current region).

As someone who is responsible for performing code reviews, I found this quite frustrating in that I couldn't at a glace see how many PR's are waiting for my review and thus started to fall behind in making those reviews. As you may know from my earlier blog entries, one thing I love about AWS is that almost anything can be scripted using their API or CLI interfaces.

Using the excellent <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html">Boto3</a> Python library, I managed to create the below script which I find useful for summarising all outstanding pull requests in the account.

<a href="https://gist.github.com/MattHealy/d9a73f32a19b426bb440770edc2c9da7">View on GitHub</a>

    import boto3
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--repo', metavar='repo', type=str,
        help='Optionally filter by repository')

    args = parser.parse_args()
    filterRepository = args.repo

    client = boto3.client('codecommit')
    region = client.meta.region_name

    pullRequests = []

    resp = client.list_repositories()
    repositories = resp['repositories']

    for r in repositories:

        if filterRepository:
            if r['repositoryName'] != filterRepository:
                continue

        resp = client.list_pull_requests(
            repositoryName=r['repositoryName'],
            pullRequestStatus='OPEN',
        )

        pullRequestIds = resp['pullRequestIds']
        for p in pullRequestIds:
            pullRequests.append(p)

    for i in pullRequests:

        resp = client.get_pull_request(
            pullRequestId=i
        )

        pr = resp['pullRequest']

        title = pr['title']
        description = pr.get('description')
        lastActivity = pr['lastActivityDate']
        created = pr['creationDate']
        authorArn = pr['authorArn']

        targets = pr['pullRequestTargets']

        for t in targets:

            repo = t['repositoryName']

            link = 'https://{}.console.aws.amazon.com/codesuite/'.format(region) + \
                   'codecommit/repositories/{}/pull-requests/'.format(repo) + \
                   '{}?region={}'.format(i, region)

            print("\nLink:\n{}".format(link))

            print("\nRepo: {}".format(t['repositoryName']))
            print("Source branch: {}".format(t['sourceReference']))
            print("Target branch: {}\n".format(t['destinationReference']))

        print("Created: {}".format(created))
        print("Last Activity: {}".format(lastActivity))
        print("Author: {}\n".format(authorArn))

        print("Title: {}".format(title))
        print("Description: {}\n".format(description))

        print("------------------------------------------------------")
