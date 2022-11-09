from sync_buddy.scripts.variable import Variable
from sync_buddy.scripts.variables import Variables

def test_variable():
    variables = Variables()
    variable = Variable('${my_var}', variables)

    assert str(variable) == '${my_var}'

    variables.load_variables(my_var=6)
    assert str(variable) == '6'
