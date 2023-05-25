class Car:
    def __init__(self, x: int, y: int):
        # Passed parameters
        self.x = x
        self.y = y

        # Hard coded variables
        self.width = 1
        self.height = 1
        self.points = 0

    def action(self, choice: int):
        match choice:
            case 0:
                break

            
