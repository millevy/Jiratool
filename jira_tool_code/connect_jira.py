from __future__ import annotations

from collections import Counter
from typing import cast

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
import pprint
import datetime


def main():
    days = input("How many days have past since last comment? ")
    days_since_last_comment = int(days)
    current_date = datetime.datetime.now(datetime.timezone.utc)

    jira = JIRA(
        token_auth="MjAyNDY5NzUwOTA1OmVX7Er5UXYXUK8kU/9XJ0+CUplJ",
        server="https://issues.redhat.com",
    )

    issues = cast(ResultList[Issue], jira.search_issues("labels = sec-test-18Q2"))
    results_dict = {}
    for issue in issues:
        days_delta = 0
        no_comments = False
        if issue.fields.status.name == "Closed":
            continue

        if issue.fields.comment.comments:
            last_comment = issue.fields.comment.comments[-1]
            date_of_last_comment = datetime.datetime.strptime(last_comment.updated, "%Y-%m-%dT%H:%M:%S.%f%z")
            delta = current_date - date_of_last_comment
            days_delta = delta.days
        else:
            no_comments = True
        if no_comments or days_delta >= days_since_last_comment:
            results_dict[issue.key] = {"Summary": issue.fields.summary,
                                   "Assignee": issue.fields.assignee.displayName if issue.fields.assignee else "NA", "Days since last comment": days_delta, "Jira link": issue.permalink()}
        #import ipdb; ipdb.set_trace()
    pprint.pprint(results_dict)


if __name__ == "__main__":
    main()