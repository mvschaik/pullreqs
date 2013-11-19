import sys
import time
import os
from collections import defaultdict
from threading import Thread, active_count

from github import Github, GithubException


def main():
    gh = Github(os.environ.get('GITHUB_TOKEN'))

    org = get_organization(gh, sys.argv[1] if len(sys.argv) > 1 else None)

    print "Fetching repositories..."

    # We collect the PR's into a dict from repo name to list of PR
    prc = defaultdict(list)
    n = 0
    for repo in org.get_repos():
        t = Thread(target=get_pull_requests, args=(repo, prc))
        t.daemon = True
        t.start()
        n += 1

    while active_count() > 1:
        show_progress(n - active_count(), n)
        time.sleep(1)

    # Complete progress bar
    show_progress(n, n)
    print

    show_report(prc)


def get_organization(gh, name=None):
    if name:
        try:
            return gh.get_organization(name)
        except GithubException as e:
            if e.status != 404:
                raise
            print "Organization %s not found!" % name
            sys.exit(1)

    return gh.get_user()


def get_pull_requests(repo, prc):
    # PRs are issues
    if repo.fork:
        return
    if not repo.has_issues:
        return
    if repo.open_issues_count == 0:
        return

    for issue in repo.get_issues():
        # This determines if it is a pull request
        if _is_pull_request(issue):
            prc[repo.name].append(issue)


def show_report(prc):
    if len(prc.values()) == 0:
        print "No pull requests found!"
        return

    title_len = max(len(pr.title) for prs in prc.values() for pr in prs)
    url_len = max(len(pr.html_url) for prs in prc.values() for pr in prs)

    for repo, prs in prc.iteritems():
        print "====", repo, "===="
        for pr in prs:
            print "%s\t%s" % (pr.title.ljust(title_len), pr.html_url.ljust(url_len))


def show_progress(n, total):
    print "\r[%s>%s] (%d/%d)" % (n * '=', (total - n) * '-', n, total),
    sys.stdout.flush()


def _is_pull_request(issue):
    # Existence of html_url determines if the issue is a PR
    return issue.pull_request.html_url


if __name__ == '__main__':
    main()
