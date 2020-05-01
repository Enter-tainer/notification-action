import json


def message(e, messageFormat):
    if messageFormat == 'markdown':
        commits = e['commits']
        forced = bool(e['forced'])
        compareUrl = e['compare']
        repoName = e['repository']['full_name']
        repoUrl = e['repository']['html_url']
        pusherName = e['pusher']['name']
        ref = e['ref']
        if ref[:11] == 'refs/heads/':
            ref = '[{0}]({1}/tree/{0})'.format(ref[11:], repoUrl)
        elif ref[:10] == 'refs/tags/':
            ref = '[{0}]({1}/releases/tag/{0})'.format(ref[10:], repoUrl)
        message = '{} {}pushed [{} commit{}]({}) to [{}]({}):{}:\n\n'.format(
            pusherName, 'forced-' if forced else '', len(commits), 's' if len(commits) >= 2 else '', compareUrl, repoName, repoUrl, ref)
        for commit in commits:
            shortSHA = commit['id'][:7]
            url = commit['url']
            author = commit['author']['name']
            commitMessage = commit['message']
            message += '[{}]({}) - {} by.{}  \n'.format(shortSHA,
                                                        url, commitMessage, author)
        return message

    elif messageFormat == 'plaintext':
        commits = e['commits']
        forced = bool(e['forced'])
        repoName = e['repository']['full_name']
        pusherName = e['pusher']['name']
        ref = e['ref']
        if ref[:11] == 'refs/heads/':
            ref = '{}'.format(ref[11:])
        elif ref[:10] == 'refs/tags/':
            ref = '{}'.format(ref[10:])
        message = '{} {}pushed {} commit{} to {}:{}:\n\n'.format(
            pusherName, 'forced-' if forced else '', len(commits), 's' if len(commits) >= 2 else '', repoName, ref)
        for commit in commits:
            shortSHA = commit['id'][:7]
            author = commit['author']['name']
            commitMessage = commit['message']
            message += '{} - {} by.{}\n'.format(shortSHA,
                                                commitMessage, author)
        return message

    else:
        raise Exception(
            'The format {} is unsupported for the event push'.format(format))
