session = Session()

for data in pagination.max_count(endpoints.search):
    for item in data['articles']:
        n = News(
            title=item['title'],
            description=item['description'],
            content=item['content'],
            url=item['url'],
            image=item['image'],
            published_at=formatters.datetime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
            source=Source(
                name=item['source']['name'],
                url=item['source']['url']
            )
        )
        session.add(n)
session.commit()
