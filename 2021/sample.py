
# Foobar
def foobar(x):
    return x + 1

class Car:
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.position = 0
        self.direction = 0

    def move(self, speed, direction):
        self.speed = speed
        self.direction = direction
        self.position += speed * direction
    
    def __str__(self):
        return self.name + ': ' + str(self.position)
