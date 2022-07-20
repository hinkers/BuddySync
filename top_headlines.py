session = Session()

for item in data['articles']:
    n = News(
        title=item['title'],
        url=item['url'],
        publishedat=datetime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    )
    session.add(n)
session.commit()
