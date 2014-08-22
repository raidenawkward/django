'''
    define user for login
'''

from jconfig import JConfig

class User(JConfig):
    '''
    uniform user information
    with save/load support
    '''

    GLOBAL_ID = 0

    def __init__(self):
        JConfig.__init__(self)
        self._id = User.GLOBAL_ID
        User.GLOBAL_ID += 1


    def getId(self):
        return self._id


    def setId(self, id):
        self._id = id



if __name__ == '__main__':
    u1 = User()
    '''u1.setAttr('name', 'alex')
    u1.setAttr('email', 'alex@test.com')'''
    u1.loadFromFile('test.user')

    u2 = User()
    '''u2.setAttr('name', 'baal')
    u2.setAttr('email', 'baal@test.com')
    u2.loadFromFile('u2.json')'''

    print(u1.toString())
    print(u2.toString())

    #u1.saveToFile('u1.json')
    #u2.saveToFile('u2.json')
