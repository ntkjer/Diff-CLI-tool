import click

from click_datetime import Datetime
from click_flexpath import Flexpath
from helper_lib import *


#TODO chagne sys.argv[-1] to handle --help flag
@click.command()
@click.option('--field', '-f', 
              type=click.Choice(['schedule', 'ambientTemp']), 
              multiple=True
              )
@click.argument('path',
              type=Flexpath(date=validate_date(sys.argv[-1], format='%Y-%m-%dT%H:%M'))
              )
@click.argument('timestamp', 
              type=Datetime(format='%Y-%m-%dT%H:%M'),
              default=datetime.now()
              )
def cli(field, path, timestamp):
    """
    ####################################################################
 
    .__________________________________________________________________.\n
    |                    Formatting for Arguments                      |\n
    |         Argument                |       Required Format          |\n
    |==================================================================|\n
    |        timestamp <TS>           |         <%Y-%m-%dT%H:%M>       |\n
    |==================================================================|\n
    |        path <path>              | <path/to/directory> OR         |\n
    |                                 |   <s3/aws/link/to/path>        |\n
    |_________________________________|________________________________|\n

    \b

    ####################################################################\n
    \b
    .__________________________________________________________________.\n
    |..................................................................|\n
    |                     Formatting for Options                       |\n
    |__________________________________________________________________|\n
    |         Field                   |           Usage                |\n
    |==================================================================|\n
    |        <param>                  |         --field/-f             |\n
    |==================================================================|\n
    |        Available fields: schedule, ambientTemp, setTemp          |\n
    |                                                                  |\n
    |        Info: Enter your prefered fields as --field/-f <field>    |\n
    |       -------------------------------------------------------    |\n
    |        Usage: You may enter multiple fields, as long as you      |\n
    |               specify the parameter before with a -f/--field tag |\n
    |       --------------------------------------------------------   |\n
    |    Example (1) : replay --field ambientTemp <path/to/data> <TS>  |\n
    |    (2 or more) : replay -f ambientTemp -f setTemp <path> <TS>    |\n
    |..................................................................|\n
    |__________________________________________________________________|\n
    """
    #TODO: 
    # -remove logical evals and create helper functions
    # -remove string checking and create helper func
    # -> 
    if ".gz" not in path:
        path = make_file_from_time(timestamp, path)
    data = get_boundary_data(timestamp, path)
    if len(data) == 0:
        click.echo("404 Not Found")
        sys.exit(1)
    else:
        key = select_closest_bound(data)
        result = get_state(key, data, field)
        output = build_state(result, timestamp)
        click.echo(json.dumps(output))

  

 


