from collections import defaultdict
from github import Github, GithubException
import sys
import time
from threading import Thread, active_count
import os


def progress(n, total):
    print "\r[%s>%s] (%d/%d)" % (n * '=', (total - n) * '-', n, total),
    sys.stdout.flush()


def get_prs(repo, prs):
    if repo.source:
        # Forked from other repo
        return
    if not repo.has_issues:
        return
    if repo.open_issues_count == 0:
        return
    for issue in repo.get_issues():
        if issue.pull_request.html_url:
            prs[repo.name].append(issue)


def print_report(prs):
    if len(prs.values()) == 0:
        print "No pull requests found!"
        return

    title_len = max(len(r.title) for rs in prs.values() for r in rs)
    url_len = max(len(r.html_url) for rs in prs.values() for r in rs)

    for repo, rs in prs.iteritems():
        print "====", repo, "===="
        for r in rs:
            print "%s\t%s" % (r.title.ljust(title_len), r.html_url.ljust(url_len))


def get_organization(g, name=None):
    if name:
        try:
            return g.get_organization(name)
        except GithubException as e:
            if e.status != 404:
                raise
            print "Organization %s not found!" % name
            sys.exit(1)

    return g.get_user()


def main():
    g = Github(os.environ.get('GITHUB_TOKEN'))

    org = get_organization(g, sys.argv[1] if len(sys.argv) > 1 else None)

    print "Fetching repositories..."

    prs = defaultdict(list)
    for repo in org.get_repos():
        t = Thread(target=get_prs, args=(repo, prs))
        t.daemon = True
        t.start()

    nrepos = org.total_private_repos + org.public_repos
    while active_count() > 1:
        progress(nrepos - active_count(), nrepos)
        time.sleep(1)

    progress(nrepos, nrepos)
    print

    print_report(prs)


if __name__ == '__main__':
    main()
