from datetime import datetime as dt


class Formatters:

    @staticmethod
    def datetime(d_str, s_format=None):
        return dt.strptime(d_str, s_format if s_format is not None else '%Y-%m-%d %H:%M:%S')
