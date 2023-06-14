
from game.components.enemies.ship import Ship
class EnemyHandler:
    def __init__(self) -> None:
        self.enemies = []
        self.enemies.append(Ship())

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self,screen):
        for enemy in self.enemies:
            enemy.draw(screen)