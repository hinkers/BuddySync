session = Session()

for item in data:
    fish_data = dict()
    for key in item:
        c_name = key.replace(' ', '').replace(',', '')
        if c_name in Fish.__columns__:
            fish_data[c_name] = item[key]
    session.add(Fish(**fish_data))
session.commit()
