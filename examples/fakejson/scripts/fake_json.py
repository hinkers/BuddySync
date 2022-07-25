session = Session()

session.add(Person(
    id=data['id'],
    email=data['email'],
    gender=data['gender'],
    login=Login(
        date_time=formatters.datetime(data['last_login']['date_time'], '%a %b %d %H:%M:%S UTC %Y'),
        ip4=data['last_login']['ip4']
    )
))

session.commit()
success = True