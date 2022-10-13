from os.path import exists

from schema import And, Schema


def validate_variables(data):
    return Schema({str: object}).validate(data)


def validate_script(script):
    if exists(script):
        return True
    return False


def validate_scripts(data):
    return Schema([And(str, validate_script)]).validate(data)

