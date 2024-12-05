
class Entite :
    def __init__(self, tmx_map) -> None:
        self.life = 100
        self.alive = True

        self.map_width = tmx_map.width * tmx_map.tilewidth
        self.map_height = tmx_map.height * tmx_map.tileheight
    
    def prendre_degat(self, dégat):
        self.life-=dégat
        if self.life<=0:
            self.alive =False

    def despawn(self):
        if self.alive!=True:
            print("tu es mort ")

    def position():
        print("position")
    
    def avancer(self):
        if self.y-5 >= 0 :
            self.y -= 5
            self.rect.y = self.y

    def droite(self):
        if self.x + 5 + self.rect.width <= self.map_width: 
            self.x += 5
            self.rect.x = self.x

    def gauche(self):
        if self.x -5 >= 0:
            self.x -= 5
            self.rect.x = self.x

    def bas(self): 
        if self.y + 5 + self.rect.height <= self.map_height:
            self.y += 5
            self.rect.y = self.y
    
    