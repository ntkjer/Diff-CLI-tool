import click

from click_datetime import Datetime
from click_flexpath import Flexpath
from helper_lib import *


OPTION_FIELDS = ['schedule', 'ambientTemp', 'heatTemp']

@click.command(options_metavar='<options>',
               )
@click.option('--field', '-f', 
              type=click.Choice(OPTION_FIELDS), 
              multiple=True
              )
@click.argument('path',
              type=Flexpath(date=validate_date(sys.argv[-1], format='%Y-%m-%dT%H:%M')),
              metavar='[<path/to/local>|<link/to/s3>]'
              )
@click.argument('timestamp', 
              type=Datetime(format='%Y-%m-%dT%H:%M'),
              default=datetime.now(),
              metavar = '[timestamp]'
              )
def cli(field, path, timestamp):
    """
    NAME:\n
        replay : infer the state from diffs in the EnergyHub dataset.\n
    \n
    \b
    SYNOPSIS:\n
    \n
        replay: [--field|-f] [FIELD_OPTION] [local_files|s3_link] [timestamp]\n
    \b
    DESCRIPTION:\n
        replay infers the state from diffs in the EnergyHub dataset.\n
        The dataset can be retrieved either through local path specification, or by specifying an s3 link. \n
    \n
        The first synopsis option details the general approach to usage. We can indicate each field with --field or -f, following the field name of choice. \n
        The number of fields do not matter, and you can use as many as you need. However, please be mindful of the fields available to the user.\n
        Available fields can be seen at the bottom of this doc, specified as "Options".
    \n
        Required arguments are path and timestamp.\n
        Path can be specified as either a local path or s3 link. The s3 link expects the exact link specified in the example. \n
        Timestamp is required to be positioned at the tail of the command.\n
    \b
    EXAMPLES:\n
        $replay --field ambientTemp --field schedule /tmp/ehub_data 2016-01-01T03:00\n
        >>{"state": {"ambientTemp": 77.0, "schedule": false}, "ts": "2016-01-01T03:00:00"}\n
        $replay --field ambientTemp --field schedule s3://net.energyhub.assets/public/dev-exercises/audit-data/ 2016-01-01T03:00\n
        >>{"state": {"ambientTemp": 77.0, "schedule": false}, "ts": "2016-01-01T03:00:00"}
    \b
    """
    is_s3 = is_s3_link(path)
    path = check_extension(timestamp, path)
    data = get_boundary_data(timestamp, path)
    empty = is_data_empty(data)
    if empty:
        if is_s3:
            click.echo("404 not found")
        else:
            click.echo("****Invalid entry****")
            click.echo("Usage: replay --help")
    else:
        key = select_closest_bound(data)
        result = get_state(key, data, field)
        output = filter_state(result, timestamp)
        click.echo(json.dumps(output))


  

 


