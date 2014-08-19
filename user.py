'''
    define user for login
'''

import json

class User:
    '''
    uniform user information
    with save/load support
    '''

    GLOBAL_ID = 0

    def __init__(self):
        self._id = User.GLOBAL_ID
        User.GLOBAL_ID += 1
        self._attr = {}

    def getId(self):
        return self._id

    def setId(self, id):
        self._id = id

    def getAttrDict(self):
        return self._attr

    def setAttrDict(self, d):
        self._attr = d

    def getAttr(self, key):
        try:
            res = self._attr[key]
        except:
            res = None

        return res

    def setAttr(self, key, value):
        self._attr[key] = value

    def toString(self):
        res = ''
        res += '{\n'

        d = self.getAttrDict()

        i = 0
        for (k, v) in d.items():
            res += '\"' + k + '\":\"' + v + '\"'
            if i != len(d) - 1:
                res += ','
            res += '\n'
            i += 1

        res += '}\n'

        return res

    def loadFromFile(self, file):
        with open(file) as f:
            res = True
            try:
                config = json.load(f)
                self.setAttrDict(config)
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
    u1 = User()
    '''u1.setAttr('name', 'alex')
    u1.setAttr('email', 'alex@test.com')'''
    u1.loadFromFile('u1.json')

    u2 = User()
    '''u2.setAttr('name', 'baal')
    u2.setAttr('email', 'baal@test.com')'''
    u2.loadFromFile('u2.json')

    print(u1.toString())
    print(u2.toString())

    #u1.saveToFile('u1.json')
    #u2.saveToFile('u2.json')
