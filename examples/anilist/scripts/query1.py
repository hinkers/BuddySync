session = Session()

media = data['data']['Media']

session.add(Anime(
    id=media['id'],
    english_title=media['title']['english'],
    native_title=media['title']['native'],
    romaji_title=media['title']['romaji']
))

session.commit()
success = True
