import math
import random
import sys

import pygame

from pythonProject.ai_system.fuzzy import landing_sim


# TODO rozbic klasy na oddzielne pliki
# to nie byl najlepszy pomysl by miec wszystko w jednym

class GameObject:
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
        self.angle = 0.0
        self.debug_mode = False

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
        self.thrust_power = 0.10

        self.image = pygame.image.load("pythonProject/gameplay/rocket.png").convert_alpha()
        self.image_width = 50
        self.image_height = 100
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.original_image = self.image

        self.collision = self.image.get_rect(topleft=(self.xPos, self.yPos))

        self.show_fire = False
        self.fire_color = (255, 0, 0)
        self.fire_width = 50
        self.fire_height = 20

    def normalizeValues(self):
        if self.angle > 180:
            self.angle = -179
        if self.angle < -179:
            self.angle = 180


    def update(self, gravity=0.0003):
        self.normalizeValues()
        print(f"Input thrust_power={self.getThrustPower()}, angle={self.getAngle()}, deltaY={self.getDeltaY()}, deltaX={self.deltaX} ")
        print(f"X={self.xPos}, Y={self.yPos}")

        landing_sim.input['posX'] = self.xPos
        # landing_sim.input['posY'] = self.yPos
        landing_sim.input['angle'] = self.angle
        landing_sim.input['velocityX'] = self.deltaX
        landing_sim.input['velocityY'] = self.deltaY
        landing_sim.compute()
        delta_angle_output = landing_sim.output.get('deltaAngle')
        delta_control_output = landing_sim.output.get('thrustControl')
        if delta_angle_output is None:
            delta_control_output = 0.0

        print(f"deltaAngle={delta_angle_output}, thrustControl={delta_control_output}")
        print(landing_sim.output)
        self.angle += landing_sim.output['deltaAngle']
        # if self.fuel > 0:
        #     self.fuel -= 0.4
        #     self.thrust_power += landing_sim.output['thrustControl']
        #     rad = math.radians(self.angle)
        #     self.deltaX += self.thrust_power * math.sin(rad)
        #     self.deltaY -= self.thrust_power * math.cos(rad)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 2

        if keys[pygame.K_RIGHT]:
            self.angle += 2

        if keys[pygame.K_UP]:
            if self.fuel > 0:
                self.fuel -= 0.4
                self.thrust_power += 0.1
                rad = math.radians(self.angle)
                self.deltaX += self.thrust_power * math.sin(rad)
                self.deltaY -= self.thrust_power * math.cos(rad)
        else:
            if self.thrust_power > 0:
                self.thrust_power -= 0.01
            else:
                self.thrust_power = 0

        if keys[pygame.K_UP]:
            self.show_fire = True
        else:
            self.show_fire = False

        self.deltaY += gravity
        self.xPos += self.deltaX
        self.yPos += self.deltaY

        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        self.collision = rotated_image.get_rect(center=(self.xPos, self.yPos))

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.xPos, self.yPos))

        screen.blit(rotated_image, rotated_rect.topleft)

        if self.show_fire:
            fire_x = self.xPos - (self.fire_width // 2)
            fire_y = rotated_rect.bottom

            fire_surface = pygame.Surface((self.fire_width, self.fire_height), pygame.SRCALPHA)

            fire_surface.fill(self.fire_color)
            fire_surface.set_alpha(128)

            fire_surface = pygame.transform.rotate(fire_surface, -self.angle)
            fire_rect = fire_surface.get_rect(center=(fire_x + (self.fire_width / 2), fire_y + self.fire_height/2))
            screen.blit(fire_surface, fire_rect.topleft)

        if self.debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.collision, 2)

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
        if self.debug_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

    def check_collision(self, Rocket):
        return self.rect.colliderect(Rocket.collision)

    def check_landing(Rocket):
        print("Check angle...")
        return False


class Tlo(GameObject):
    def __init__(self, xPos, yPos, Rocket):
        super().__init__(xPos, yPos)
        self.font = pygame.font.Font(None, 36)
        self.rocket = Rocket

    def draw(self, screen):
        text = f"""fuel: {self.rocket.getFuel():.2f}
        angle: {self.rocket.getAngle():.2f}
        deltaY: {self.rocket.getDeltaY():.2f}"""
        text_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

class GameManager:
    def __init__(self,sWidth,sHeight,x=400,y=50):
        self.terrain_lins = list()
        self.rocket = Rocket(x,y)
        self.SCREEN_HEIGHT = sHeight
        self.SCREEN_WIDTH = sWidth
        self.tlo = Tlo(0,0,self.rocket)

    def generate_random_terrain(self,num_terrains,):
        terrain_list = []
        for _ in range(num_terrains):
            x = random.randint(0, self.SCREEN_WIDTH - 100)
            width = random.randint(50, 200)
            y = self.SCREEN_WIDTH - random.randint(20, 100)
            # can_land = random.choice([True, False])
            terrain = Teren(x, y, width, 10, True) # Tryb debug - należałoby zaimplementować wykrywanie ścieżki do terenu do lądowania
            terrain_list.append(terrain)

        return terrain_list

def main(sWidth, sHeight, fuzzy):
    pygame.init()
    (SCREEN_WIDTH,SCREEN_HEIGHT) = sWidth, sHeight
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lunar Lander with fuzzy logic")
    clock = pygame.time.Clock()

    gameManager = GameManager(SCREEN_WIDTH,SCREEN_HEIGHT,random.randint(50, SCREEN_WIDTH-50), 50)
    rakieta = gameManager.rocket

    teren = gameManager.generate_random_terrain(20)

    tlo = gameManager.tlo

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
                        if rakieta.deltaY > 1 & (rakieta.angle < 3.0) & (rakieta.angle > -3.0):
                            print("Katastrofa lotnicza")
                            # if teren_obj.check_landing(rakieta):
                        else:
                            print("Sukces")
                    else:
                        print("Katastrofa lotnicza tu nie mozna ladowac")

                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
