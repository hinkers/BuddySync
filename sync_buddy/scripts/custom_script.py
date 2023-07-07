from dataclasses import dataclass

from sync_buddy.scripts.formatters import Formatters
from sync_buddy.utilities.utilites import Utilities


@dataclass
class CustomScript:

    container: object
    filename: str

    def run(self, locals_=None, throw=True):
        if locals_ is None:
            locals_ = dict()

        loc = dict(
            endpoints=self.container.endpoints_as_object(),
            pagination=self.container.pagination_as_object(),
            formatters=Formatters,
            Session=None,
            variables=self.container.variables.as_dict(),
            utilities=self.container.utilities,
            **self.container.loc_tables(),
            **locals_
        )
        if len(self.container.databases) > 0:
            loc['Session'] = self.container.databases['default'].session()
        with open(self.filename, 'r') as script:
            try:
                exec(compile(script.read(), self.filename, 'exec'), dict(), loc)
            except Exception as e:
                if throw:
                    raise e
                loc['error'] = str(e)
        return loc
