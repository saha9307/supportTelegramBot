from jira import JIRA
jira = JIRA('http://jira.modern-expo.com',basic_auth=('JiraSupport', 'q1w2e3r4_5'))
try:
    issue = jira.issue('ASU-2119')
    print(issue)
except Exception as err:
    print(err)


# for c in issue.fields:
#     print(c)
# print(issue.fields)
# print(issue.fields.summary)

