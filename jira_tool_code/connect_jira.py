from __future__ import annotations
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
        token_auth="",
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
            results_dict[issue.key] = {
                "Summary": issue.fields.summary,
                "Assignee": issue.fields.assignee.displayName if issue.fields.assignee else "NA",
                "Days since last comment": days_delta,
                "Status": issue.fields.status.name,
                "Jira link": issue.permalink(),
                "labels": ", ".join(issue.fields.labels)
            }
    headers = ["Issue Key", "Summary", "Assignee", "Days since last comment", "Status", "Jira link", "labels"]
    rows = [[key] + list(value.values()) for key, value in results_dict.items()]
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    format_str = " | ".join([f"{{:<{width}}}" for width in col_widths])
    print(format_str.format(*headers))
    print("-" * (sum(col_widths) + 5 * (len(headers) - 1)))
    #import ipdb; ipdb.set_trace()
    for row in rows:
        print(format_str.format(*row))


if __name__ == "__main__":
    main()