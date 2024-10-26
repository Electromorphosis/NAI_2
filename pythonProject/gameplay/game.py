import pygame
import sys
import math

class GameObject:
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
        self.image = pygame.Surface((50, 100))
        self.image.fill((255, 255, 255))
        self.angle = 0.0

    def draw(self, screen):
        raise NotImplementedError("Subclass must implement draw method")

    def update(self):
        raise NotImplementedError("Subclass must implement update method")

class Rocket(GameObject):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos)
        self.deltaX = 0
        self.deltaY = 0
        self.fuel = 100.0
        self.thrust_power = 0.1
        self.image = pygame.image.load("pythonProject/gameplay/rocket.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.original_image = self.image


    def update(self, gravity=0.05):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 2

        if keys[pygame.K_RIGHT]:
            self.angle += 2

        if keys[pygame.K_UP]:
            if self.fuel > 0:
                self.fuel -= 0.4  #
                rad = math.radians(self.angle)
                self.deltaX += self.thrust_power * math.sin(rad)
                self.deltaY -= self.thrust_power * math.cos(rad)

        self.deltaY += gravity
        self.xPos += self.deltaX
        self.yPos += self.deltaY

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.xPos, self.yPos))
        screen.blit(rotated_image, rotated_rect.topleft)


    def getFuel(self) -> float:
        return self.fuel

    def getThrustPower(self) -> float:
        return self.thrust_power

    def getAngle(self) -> float:
        return self.angle

    def getDeltaY(self) -> float:
        return self.deltaY

class Teren(GameObject):
    def __init__(self, xPos, yPos, width, height, is_landable):
        super().__init__(xPos, yPos)
        self.rect = pygame.Rect(xPos, yPos, width, height)
        self.is_landable = is_landable
        self.color = (0, 255, 0) if is_landable else (255, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, Rocket):
        return self.rect.colliderect(Rocket.image.get_rect(topleft=(Rocket.xPos, Rocket.yPos)))

    def check_landing(Rocket):
        print("Check angle...")
        return False

class Tlo(GameObject):
    def __init__(self,xPos, yPos,Rocket):
        super().__init__(xPos, yPos)
        self.font = pygame.font.Font(None, 36)
        self.rocket = Rocket
    def draw(self,screen):
        text = f"""fuel: {self.rocket.getFuel():.2f}
        angle: {self.rocket.getAngle():.2f}
        deltaY: {self.rocket.getDeltaY():.2f}"""
        text_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))


def main(sWidth, sHeight):

    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = sWidth, sHeight
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lunar Lander with fuzzy logic")
    clock = pygame.time.Clock()

    rakieta = Rocket(400, 50)
    teren = [
        Teren(SCREEN_WIDTH/4, SCREEN_HEIGHT - 100, SCREEN_WIDTH/2 , 10, True),
        Teren(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 30, False)
    ]
    tlo = Tlo(0,0,rakieta)

    gameObjects = [rakieta, *teren, tlo]

    running = True
    while running:
        screen.fill((10, 10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        rakieta.update()
        for gameObject in gameObjects:
            gameObject.draw(screen)

            for teren_obj in teren:
                if teren_obj.check_collision(rakieta):
                    if teren_obj.is_landable:
                        #if teren_obj.check_landing(rakieta):
                        print("Landing")
                        running = False


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
