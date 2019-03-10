import functools32, sys, json, jsonlines, gzip, ast, os, subprocess, click
from requests.exceptions import HTTPError


from datetime import datetime
from subprocess import Popen, PIPE, call
import datetime as dt




@functools32.lru_cache(maxsize=128)
def download_S3(link, path='/tmp/ehub_data/'):
    try:
        link = link[:-1]
        db_extension = '.tar.gz'
        filename = path + '/' + 'audit-data.tar.gz'
        process = subprocess.Popen('mkdir '+ path + ' && cd ' + path, shell=True, stdout=subprocess.PIPE).wait()
        process = subprocess.Popen('aws s3 cp ' + link + db_extension + ' ' + path, shell=True, stdout=subprocess.PIPE).wait()
        subprocess.call(["tar", "xzf", filename, "-C", path])
        return path
    except requests.exceptions.HTTPError as err:
        print "404 Not Found"
        sys.exit(1)

def check_extension(timestamp, filepath):
    if ".gz" not in filepath:
        filepath = make_file_from_time(timestamp, filepath)
    return filepath

def is_data_empty(data):
    return len(data) == 0


def handle_input_date(date):
    options = ["--help", "-h", "help"]
    if date in options:
        date = None
    return date


def validate_date(date, format):
    date = handle_input_date(date)
    if date is not None:
        try:
            date = datetime.strptime(date, format)
            return date 
        except ValueError as e:
            click.echo('Could not parse datetime string "{datetime_str}" formatted as {format} ({e})'.format(
                    datetime_str=date, format=format, e=e))
    else:
        pass


def filter_state(data, timestamp):
    result = {}
    result['state'] = {}
    for k, v in data.iteritems():
        result['state'][k] = v
    result['timestamp'] = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    return result


def get_state(key, data, field):
    relevant_data = data[key]
    return retrieve_fields(field, relevant_data, key)


def retrieve_fields(field, input, option):
    result = {}
    input = ast.literal_eval(input)
    if option == "high":
        option = "before"
    else:
        option = "after"
    for f in field:
        value = input.get(option).get(f)
        if value == None:
            result[f] = "false"
        else:
            result[f] = value
    return result


def select_closest_bound(data):
    minimum = min(data['low_delta'], data['high_delta'])
    result = ""
    for k,v in data.iteritems():
        if v == minimum:
            if k == "high_delta":
                result = "high"
            else:
                result = "low"
    return result


def make_file_from_time(timestamp, path):
    year, month, day = timestamp.year, timestamp.month, timestamp.day
    year = str(year)
    month, day = sanitize_dates(month, day)
    file_extension = year + '/' + month + '/' +  day + ".jsonl.gz"
    file_name = path + '/' + file_extension
    return file_name


def make_top_dir(timestamp, path):
    year = timestamp.year
    year = str(year)
    directory = path + '/' + year
    return directory


def make_dir(timestamp, path):
    year, month = timestamp.year, timestamp.month
    year = str(year)
    month = sanitize_date(month)
    directory = path + '/' + year + '/' + month
    return directory


def does_file_exist(timestamp):
    try:
        file_extension = '.jsonl.gz'
        local_path = '/tmp/ehub_data'
        file = make_file_from_time(timestamp, local_path)
        top_directory = make_top_dir(timestamp, local_path)
        directory = make_dir(timestamp, local_path)
        isTopDirectory, isDirectory, isFile = (
                    os.path.exists(top_directory),
                    os.path.exists(directory),
                    os.path.exists(file)
        )
        if isTopDirectory:
            if isDirectory:
                if isFile:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        pass


def get_boundary_data(timestamp, path, form='%Y-%m-%dT%H:%M:%S.%f'):
    low = high = dt.timedelta(hours=100)
    d = {}
    if does_file_exist(timestamp) == True:
        with gzip.open(path) as fin:
            for line in fin:
                data = json.loads(line)
                current_time = datetime.strptime(data['changeTime'], form)
                if current_time > timestamp:
                    delta = current_time - timestamp
                    if delta <= high:
                        high = delta 
                        d['high'] = line
                        d['high_delta'] = delta
                else:
                    delta = timestamp - current_time
                    if delta <= low:
                        low = delta
                        d['low'] = line
                        d['low_delta'] = delta
    return d


def sanitize_dates(month, day):
    if month > 12 or day > 31:
        raise ValueError
    return sanitize_date(month), sanitize_date(day)


def sanitize_date(date):
    if type(date) != int:
        raise ValueError
    return sanitize_integer(date)


def sanitize_integer(value):
    if type(value) != int or value >= 31:
        raise ValueError
    if value // 12 > 0:
        result = str(value)
    else:
        value = str(value)
        result = '0' + value
    return result


