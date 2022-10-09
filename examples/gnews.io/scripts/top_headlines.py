session = Session()

for data in pagination.max_count(endpoints.top_headlines):
    for article in data['articles']:
        n = utilities.map_to(
            News,
            article,
            dict(published_at='publishedAt'),
            dict(published_at=[formatters.datetime, ['%Y-%m-%dT%H:%M:%SZ']])
        )
        session.add(n)
    break  # Lets paginate but only get the first page I guess
session.commit()

variables['test_one'] = 5
