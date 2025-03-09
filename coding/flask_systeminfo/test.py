
import os

class FileWriter:
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, filename, text):
        with open(f'{self.directory}/{self.filename}', 'w') as f:
            f.write(text)


class DumpText(FileWriter):
    def __init__(self, directory):
        super().__init__(directory)

        

userswriter = DumpText('/tmp/users')
userswriter.write('users.txt', 'user1\nuser2\nuser3\n')


domainswriter = DumpText('/tmp/domains')
domainswriter.write('domains.txt', 'domain1\ndomain2\ndomain3\n')
