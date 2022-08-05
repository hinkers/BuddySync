from dataclasses import dataclass

from container import Container
from apisync.scripts.formatters import Formatters


@dataclass
class CustomScript:

    filename: str
    container: Container

    def run(self, locals_=dict(), throw=True):
        loc = dict(
            endpoints=self.container.endpoints,
            formatters=Formatters,
            Session=self.container.sql.session(),
            **self.container.tables,
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
