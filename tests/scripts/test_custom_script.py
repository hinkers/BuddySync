import pytest

from sync_buddy.container import Container

from ..data.sqls import sql1


def test_custom_script_success(capsys, tmp_path):
    f = tmp_path / "test_script.py"
    f.write_text('print("Hello World")')

    container = Container(scripts=[f])
    
    assert len(container.scripts) == 1
    container.scripts[0].run()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Hello World'

def test_custom_script_session(capsys, tmp_path):
    f = tmp_path / "test_script.py"
    f.write_text('print(Session is not None)')

    container = Container(scripts=[f], sqls=[sql1])
    
    assert len(container.scripts) == 1
    container.scripts[0].run()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'True'

def test_custom_script_fail_capture(tmp_path):
    f = tmp_path / "test_script.py"
    f.write_text('print("Hello World)')

    container = Container(scripts=[f])
    
    assert len(container.scripts) == 1
    retval = container.scripts[0].run(throw=False)
    assert 'error' in retval
    print(retval)

def test_custom_script_fail_raise(tmp_path):
    f = tmp_path / "test_script.py"
    f.write_text('print("Hello World)')

    container = Container(scripts=[f])
    
    assert len(container.scripts) == 1
    with pytest.raises(Exception):
        container.scripts[0].run()

