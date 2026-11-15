import urllib.request, json

token = 'gLgLgLgq4s1b9c2212a9798f27810e1a2492e80f20'
url = 'https://api.github.com/repos/mattdyer/projectssite/issues?state=open'
req = urllib.request.Request(url)
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Accept', 'application/vnd.github.v3+json')
resp = urllib.request.urlopen(req)
issues = json.loads(resp.read())
print(f'Total open issues: {len(issues)}')
for issue in issues:
    print(f'#{issue["number"]}: {issue["title"]} (created: {issue["created_at"]})')
if issues:
    oldest = min(issues, key=lambda i: i['number'])
    print(f'\nOldest issue: #{oldest["number"]} - {oldest["title"]}')
    body = oldest.get('body') or '(no body)'
    print(f'Body:\n{body}')
