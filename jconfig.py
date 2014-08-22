import json

class JConfig:

    def __init__(self):
        self._dict = {}


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
            for (key, value) in d.items():
                content += '\"' + key + '\":\"' + value + '\"\n'

        content += '}\n'
        return content


    def loadFromFile(self, file):
        with open(file) as f:
            res = True
            try:
                config = json.load(f)
                self._dict = config
            except ValueError:
                res = False

        return res

    def saveToFile(self, file = None):
        content = self.toString()
        path = file
        if file == None:
            path = str(self.getId()) + '.user'

        with open(file, 'w') as f:
            try:
                f.write(content)
                res = True
            except:
                res = False

        return res




if __name__ == '__main__':
    c = JConfig()
    c.loadFromFile('test.user')
    print(c.toString())
    c.saveToFile('out.txt')
