from dataclasses import dataclass

from container import container
from formatters import Formatters


@dataclass
class CustomScript:

    filename: str

    def run(self, locals_=dict(), throw=True):
        loc = dict(
            endpoints=container.endpoints,
            formatters=Formatters,
            Session=container.sql.session(),
            **container.tables,
            **locals_
        )
        with open(self.filename, 'r') as script:
            try:
                exec(compile(script.read(), self.filename, 'exec'), dict(), loc)
            except Exception as e:
                if throw:
                    raise e
                loc['Error'] = str(e)
        return loc
