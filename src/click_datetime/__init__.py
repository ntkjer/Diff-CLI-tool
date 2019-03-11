import click

from datetime import datetime
from helper_lib import handle_input_date


class Datetime(click.ParamType):
    '''
    Creates a datetime object parsed via datatime.strptime.
    Based on @ddaws and @rytilahti's implementation <github.com/click-contrib/click-datetime/>


    Format specifiers can be found here :
    https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    '''
    name = 'date'

    def __init__(self, format):
        self.format = format

    def convert(self, value, param, ctx):

        if isinstance(value, datetime):
            return value

        try:
            datetime_value = datetime.strptime(value, self.format)
            return datetime_value
        except ValueError as e:
            self.fail('Could not parse datetime string "{datetime_str}" formatted as {format} ({e})'.format(
                        datetime_str=value, format=self.format, e=e), param, ctx)


