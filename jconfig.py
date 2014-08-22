import json

class JConfig:

    def __init__(self):
        self._dict = {}
        self._path = None


    def set(self, key, value):
        self._dict[key] = value


    def get(self, key):
        d = self.getConfig()
        try:
            value = d[key]
        except KeyError:
            value = None

        return value


    def getConfig(self):
        return self._dict


    def count(self):
        return len(self.getConfig())


    def toString(self):
        content = '{\n'
        d = self.getConfig()

        if d != None:
            i = 0
            for (key, value) in d.items():
                content += b'\"' + key + '\":\"'
                content += '' + str(value) + '\"'
                if i != len(d) - 1:
                    content += ','
                content += '\n'
                i += 1

        content += '}\n'
        return content


    def getPath(self):
        return self._path


    def loadFromFile(self, file):
        self._path = file

        with open(file) as f:
            res = True
            try:
                config = json.load(f)
                self._dict = config
                f.close()
            except ValueError:
                res = False

        return res

    def saveToFile(self, file = None):
        self._path = file

        content = self.toString()
        path = file
        if file == None:
            return False

        with open(file, 'w') as f:
            try:
                f.write(content)
                res = True
                f.close()
            except:
                res = False

        return res




if __name__ == '__main__':
    c = JConfig()
    c.loadFromFile('test.user')
    print(c.toString())
    c.saveToFile('out.txt')
