import click
import os.path

from werkzeug import abort
from helper_lib import *


class Flexpath(click.ParamType):

    name = 'path_string'

    def __init__(self, date):
        self.date = date
        self.path = None


    def setPath(self, path):
        self.path = path


    def convert(self, path, param, ctx):
        try:
            if path == '/tmp/ehub_data':
                self.setPath(path)
                return path
            elif path == 's3://net.energyhub.assets/public/dev-exercises/audit-data/':
                localPath = self.getLocalPath()
                if localPath == None:
                    download_path = download_S3(path)
                    self.setPath(download_path)
                    return download_path
                else:
                    print localPath
                    self.setPath(localPath)
                    return localPath
            else:
                return path
        except:
            abort(404)


    def getLocalPath(self):
        file = None
        try:
            file_extension = '.jsonl.gz'
            local_path = '/tmp/ehub_data'
            file = make_file_from_time(self.date, local_path)
            if does_file_exist(self.date) == True:
                return file
        except:
            return file
            raise ValueError
