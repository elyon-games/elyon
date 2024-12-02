class arme:
    def __init__(self, dégat, durabilité):
        self.dégat = dégat
        self.durabilité = durabilité

    def attaquer(self):
        print(f"j'attaque: -{self.dégat}")