import time

import pygame, os, inspect, math, random
from pygame.transform import scale

pygame.init()

# creer une police qui permet d afficher a la fin win
police = pygame.font.SysFont("times new roman", 45)
police_health = pygame.font.SysFont("times new roman", 15)
police_crew = pygame.font.SysFont("times new roman", 25)
police_timer = pygame.font.SysFont("times new roman", 20)

# recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data2")

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = int(9 * SCREEN_WIDTH / 16) - 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BroForce du Wish')

fond = pygame.image.load(os.path.join(assets, "Collision30000.png"))
fond_save = fond
map = pygame.image.load(os.path.join(assets, "Map0000.png"))

# selection de l'equipe au debut
red = False
green = False
print_m = False

# IMPORTATION POUR L ECRAN D ACCUEIL -----------------------------------------------------------------------------------
# boutton play
play_button = pygame.image.load(os.path.join(assets, "unnamedB.png"))
play_button = scale(play_button, (300, 150))
rect_button = play_button.get_rect()
rect_button.x = math.ceil(screen.get_width() / 2 - play_button.get_width() / 2)
rect_button.y = math.ceil(screen.get_height() / 2 - play_button.get_height() / 2 + 100)

# boutton red
red_button = pygame.image.load(os.path.join(assets, "unnamedR.png"))
red_button = scale(red_button, (100, 50))
red_button.set_colorkey(red_button.get_at((0, 0)))
red_button_rect = red_button.get_rect()
red_button_rect.x = 20
red_button_rect.y = 50

# boutton green
green_button = pygame.image.load(os.path.join(assets, "unnamedG.png"))
green_button = scale(green_button, (100, 50))
green_button.set_colorkey(green_button.get_at((0, 0)))
green_button_rect = green_button.get_rect()
green_button_rect.x = 20
green_button_rect.y = 100

# boutton purple
purple_button = pygame.image.load(os.path.join(assets, "unnamedP.png"))
purple_button = scale(purple_button, (300, 150))
purple_button.set_colorkey(purple_button.get_at((0, 0)))
purple_button_rect = purple_button.get_rect()
purple_button_rect.x = math.ceil(screen.get_width() / 2 - purple_button.get_height() / 2 - 70)
purple_button_rect.y = math.ceil(screen.get_height() / 2 - purple_button.get_height() / 2)

# banniere du jeu
banner = pygame.image.load(os.path.join(assets, "Broforce-logo.png"))
banner.set_colorkey(banner.get_at((0, 0)))

# fond de l ecran d accueil
reception_fond = pygame.image.load(os.path.join(assets, "monde.jpg"))

# variables du jeu
red_ladder = fond.get_at((746, 383))
gravity = 0.75
bullet_image = pygame.image.load(os.path.join(assets, "bullet.png")).convert_alpha()
timer = 0


# dessine l arriere plan
def draw_background():
    screen.blit(fond, (0, 0), area=zonejaune)
    screen.blit(map, (0, 0), area=zonejaune)


# scrolling
ZJ_xdecor = 0
ZJ_ydecor = 0

# drapeau
xflag = 1360

# Condition boucle
is_game_playing = False
running = True
end = False
won = False

# defini le raffraichissement de la page
clock = pygame.time.Clock()
FPS = 60

# actions du joueur
moving_left = False
moving_right = False
moving_down_ladder = False
moving_up_ladder = False
shoot = False


class Soldier(pygame.sprite.Sprite):

    def __init__(self, eORa, x, y, scale, speed, bot):
        pygame.sprite.Sprite.__init__(self)
        self.bot = bot
        self.cooldown = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_cooldown = 0
        self.falling_death = False
        self.decal = 0
        self.health = 100
        self.scale = scale
        self.alive = True
        self.state = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.flip = False
        self.speed = speed
        self.index = 0
        self.animation_list = []
        if eORa:
            # charge nos animations alliees dans une liste
            temp_list = []
            for i in range(5):
                img = pygame.image.load(os.path.join(assets, f"{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(6):
                img = pygame.image.load(os.path.join(assets, f"{i}r.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            img = pygame.image.load(os.path.join(assets, "0j.png")).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(8):
                img = pygame.image.load(os.path.join(assets, f"{i}d.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        else:
            # charge nos animations ennemies dans une liste
            temp_list = []
            for i in range(5):
                img = pygame.image.load(os.path.join(assets, f"{i}e.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(6):
                img = pygame.image.load(os.path.join(assets, f"{i}er.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            img = pygame.image.load(os.path.join(assets, "0ej.png")).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(8):
                img = pygame.image.load(os.path.join(assets, f"{i}ed.png")).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.state][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()

    def update(self):
        self.update_animation()
        if self.health <= 0:
            self.health = 0
            self.alive = False
        if self.cooldown > 0:
            self.cooldown -= 1

    def move(self, moving_left, moving_right, moving_down_ladder, moving_up_ladder):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -9
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        dy += self.vel_y

        c1 = fond.get_at((int(self.rect.centerx + ZJ_xdecor), int(self.rect.centery + self.rect.height / 2 - 1)))
        bc = fond.get_at((int(self.rect.centerx + ZJ_xdecor), int(self.rect.y + self.rect.height + 3)))

        # collisions du joueur
        for i in range(self.rect.y, self.rect.y + self.rect.height):
            left = fond.get_at((self.rect.x + ZJ_xdecor + dx, i))
            right = fond.get_at((self.rect.x + ZJ_xdecor + self.rect.width + dx, i))
            if left == (0, 0, 0) or right == (0, 0, 0):
                if self.bot:
                    self.direction *= -1
                else:
                    dx = 0
                break

        left2 = fond.get_at((self.rect.x + ZJ_xdecor + dx - 5, self.rect.y + self.rect.height + 5))
        right2 = fond.get_at((self.rect.x + self.rect.width + ZJ_xdecor + dx - 5, self.rect.y + self.rect.height + 5))

        if left2 == (255, 255, 255) or right2 == (255, 255, 255):
            if self.bot:
                self.direction *= -1

        self.decal = dx

        # petit decalage pour que le personnage ne s'accroche pas aux murs
        for i in range(self.rect.x + 2, self.rect.x + self.rect.width - 2):
            top = fond.get_at((i + ZJ_xdecor, int(self.rect.y + dy)))
            bottom = fond.get_at((i + ZJ_xdecor, self.rect.y + int(self.rect.height + dy)))
            if top == (0, 0, 0) or bottom == (0, 0, 0) or bottom == red_ladder:
                dy = 0
                self.vel_y = 0
                if self.vel_y < 0:
                    self.in_air = True
                else:
                    self.in_air = False
                    break

        if c1 == red_ladder and moving_up_ladder:
            dy = -3
            self.vel_y = 0
        if bc == red_ladder and moving_down_ladder:
            dy = 3
            self.vel_y = 0
        if self.rect.y + self.rect.height + dy >= 725:
            self.alive = False
            self.falling_death = True
            self.kill()

        # mets a jour la position du soldat
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        self.image = self.animation_list[self.state][self.index]
        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animation_list[self.state]):
            if self.state == 3:
                self.index = len(self.animation_list[self.state]) - 1
            else:
                self.index = 0

    def update_statement(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def shoot(self):
        if self.cooldown == 0:
            new_bullet = Bullet(self.rect.centerx + (self.direction * 0.8 * self.rect.size[0]), self.rect.centery,
                                self.direction)
            bullet_group.add(new_bullet)
            self.cooldown = 20

    def AI(self):
        if self.alive and player.alive:
            if not self.idling and random.randint(0, 200) == 1:
                self.update_statement(0)
                self.idling = True
                self.idling_cooldown = 100

            if self.vision.colliderect(player.rect):
                self.update_statement(0)
                self.shoot()

            # si l ennemi ne voit pas le joueur
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, False, False)
                    self.update_statement(1)
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    if self.direction == 1:
                        self.flip = False
                    else:
                        self.flip = True

                else:
                    self.idling_cooldown -= 1
                    if self.idling_cooldown == 0:
                        self.idling = False

        if not self.alive:
            self.update_statement(3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # mouvements balles
        self.rect.x += self.direction * self.speed
        # regarde si les balles sont a l ecran sinon les supprime
        if self.rect.right < 0 or self.rect.left > screen.get_width():
            self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 15
                self.kill()

        for ennemy in ennemy_group:
            if pygame.sprite.spritecollide(ennemy, bullet_group, False):
                if ennemy.alive:
                    ennemy.health -= 25
                    self.kill()

        # collisions avec les murs
        for i in range(self.rect.y, self.rect.y + self.rect.height):
            left = fond.get_at((self.rect.x + ZJ_xdecor, i))
            right = fond.get_at((self.rect.x + ZJ_xdecor + self.rect.width, i))
            if left == (0, 0, 0) or right == (0, 0, 0):
                self.kill()
                break


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        prop = self.health / self.max_health

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150 * prop, 20))


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.state = 2
        self.index = 0
        self.scale = scale
        self.animationflag_list = []
        temp_list = []
        for i in range(4):
            img = pygame.image.load(os.path.join(assets, f"d{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animationflag_list.append(temp_list)
        temp_list = []
        for i in range(4):
            img = pygame.image.load(os.path.join(assets, f"e{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animationflag_list.append(temp_list)
        temp_list = []
        for i in range(1):
            img = pygame.image.load(os.path.join(assets, f"f{0}.png")).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animationflag_list.append(temp_list)
        self.image = self.animationflag_list[self.state][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()
        self.image = self.animationflag_list[self.state][self.index]

    def update_animation(self):
        self.image = self.animationflag_list[self.state][self.index]
        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animationflag_list[self.state]):
            self.index = 0

    def update_statement(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        self.update_animation()

    def draw(self):
        screen.blit(self.image, self.rect)


# groupe de balles
bullet_group = pygame.sprite.Group()
health = HealthBar(20, 40, 100, 100)

ennemy_group = pygame.sprite.Group()

# LE JEU ##############################################################################################################
# BOUCLE DE L ECRAN D ACCUEIL (TANT QUE LE JOUEUR N APPUIE PAS SUR PLAY)
while not is_game_playing:
    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event

    # affichage des differents elements sur l ecran
    screen.blit(scale(reception_fond, (1500, 900)), (0, 0))
    screen.blit(play_button, rect_button)
    screen.blit(green_button, green_button_rect)
    screen.blit(red_button, red_button_rect)
    screen.blit(banner, (screen.get_width() / 2 - banner.get_width() / 2, 30))
    zone4 = police.render("team :", True, (255, 255, 255))
    screen.blit(zone4, (20, 0))

    # test permettant de savoir si le joueur lance le jeu
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_button.collidepoint(event.pos) and (red or green):
                is_game_playing = True
            if rect_button.collidepoint(event.pos) and (not red and not green):
                print_m = True
            if green_button_rect.collidepoint(event.pos):
                print_m = False
                green = True
                red = False
            if red_button_rect.collidepoint(event.pos):
                print_m = False
                red = True
                green = False

        if event.type == pygame.QUIT:  # If user clicked close
            is_game_playing = True  # va dans la boucle du jeu
            running = False  # fini la boucle jeu donc le ferme

    if print_m:
        zone3 = police.render("You need to choose one color.", True, (255, 255, 255))
        screen.blit(zone3, (0, screen.get_height() - zone3.get_height()))

    pygame.display.flip()

if red:
    player = Soldier(False, 200, 200, 1, 1, False)
    ennemy1 = Soldier(True, 1050, 279, 1, 1, True)
    ennemy2 = Soldier(True, 500, 388, 1, 1, True)
    ennemy3 = Soldier(True, 1050, 365, 1, 1, True)
    ennemy4 = Soldier(True, 1140, 654, 1, 1, True)
    ennemy5 = Soldier(True, 1180, 475, 1, 1, True)
    ennemy6 = Soldier(True, 2000, 430, 1, 1, True)
    ennemy7 = Soldier(True, 2140, 300, 1, 1, True)
    ennemy8 = Soldier(True, 2120, 370, 1, 1, True)
else:
    player = Soldier(True, 200, 200, 1, 1, False)
    ennemy1 = Soldier(False, 1050, 279, 1, 1, True)
    ennemy2 = Soldier(False, 500, 388, 1, 1, True)
    ennemy3 = Soldier(False, 1050, 365, 1, 1, True)
    ennemy4 = Soldier(False, 1140, 654, 1, 1, True)
    ennemy5 = Soldier(False, 1180, 475, 1, 1, True)
    ennemy6 = Soldier(False, 2000, 430, 1, 1, True)
    ennemy7 = Soldier(False, 2140, 300, 1, 1, True)
    ennemy8 = Soldier(False, 2120, 370, 1, 1, True)

ennemy_group.add(ennemy1)
ennemy_group.add(ennemy2)
ennemy_group.add(ennemy3)
ennemy_group.add(ennemy4)
ennemy_group.add(ennemy5)
ennemy_group.add(ennemy6)
ennemy_group.add(ennemy7)
ennemy_group.add(ennemy8)
flag = Flag(xflag, 115, 0.5)

while running:
    clock.tick(FPS)
    zonejaune = pygame.Rect(ZJ_xdecor, ZJ_ydecor, screen.get_width(), screen.get_height())
    timer = int(pygame.time.get_ticks() / 1000)

    if player.alive:
        # changement de l'action
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_statement(2)  # 2 = jump
        elif moving_left or moving_right:
            player.update_statement(1)  # 1 = run
        else:
            player.update_statement(0)  # 0 = idle
        player.move(moving_left, moving_right, moving_down_ladder, moving_up_ladder)

    else:
        player.update_statement(3)  # 3 = death
        if player.falling_death:
            running = False
            end = True
        if player.index == 7:
            time.sleep(2)
            running = False
            end = True

    draw_background()

    # mets a jour les joueurs
    player.update()
    player.draw()

    for ennemy in ennemy_group:
        ennemy.rect.x -= player.decal
        ennemy.update()
        ennemy.AI()
        ennemy.draw()

    # affiche la sante du joueur
    zone_lp = police_health.render("Life points : " + str(player.health) + "/100", True, (255, 0, 0))
    screen.blit(zone_lp, (20, 10))
    health.draw(player.health)

    # mets a jour et dessine les balles
    bullet_group.update()
    bullet_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quitter le jeu
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_s:
                moving_down_ladder = True
            if event.key == pygame.K_z:
                moving_up_ladder = True
            if event.key == pygame.K_SPACE:
                player.jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                moving_down_ladder = False
            if event.key == pygame.K_z:
                moving_up_ladder = False
            if event.key == pygame.K_SPACE:
                player.jump = False
                flag.update_statement(1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shoot = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shoot = False

    if moving_left or moving_right:
        ZJ_xdecor += player.decal

    flag = Flag(xflag, 115, 0.5)

    if ZJ_xdecor > 800:
        flag.draw()
        flag.update()
        if moving_right or moving_left:
            xflag -= player.decal
        if -30 < player.rect.x - xflag < 0 and player.rect.y < 100:
                running = False
                end = True
                won = True

    zone_time = police.render("Time : " + str(timer) + " seconds", True, (255, 255, 255))
    screen.blit(zone_time, (screen.get_width() / 2 - zone_time.get_width() / 2, 10))

    pygame.display.flip()

while end:
    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event
    screen.fill((0, 0, 0))
    screen.blit(purple_button, purple_button_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quitter le jeu
            end = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if purple_button_rect.collidepoint(event.pos):
                end = False

    # texte de fin
    zone = police.render("MISSION ECHOUEE !", True, (255, 255, 255))
    zone2 = police.render("Vous êtes mort.", True, (255, 255, 255))
    if won:
        zone = police.render("Vous avez gagné!", True, (255, 255, 255))
        zone2 = police.render("C'était donc trop facile pour vous ? Seulement " + str(timer) + "secondes", True,
                              (255, 255, 255))
    screen.blit(zone, (screen.get_width() / 2 - zone.get_width() / 2, screen.get_height() / 2 - 250))
    screen.blit(zone2, (screen.get_width() / 2 - zone2.get_width() / 2, screen.get_height() / 2 - 200))

    pygame.display.flip()

pygame.quit()

# credits : #########################################################################################################

# projet réalisé dans le cadre d'un atelier a l'esiee paris. 2020/2021 (at5-3)
# soldats en open sources : https://secrethideout.itch.io/team-wars-platformer-battle?download
# realise a l'aide des videos des chaines : graven youtube et coding with russ
# realise avec des connaissances de cours egalement
# merci a BUZER Lilian & PERRET Benjamin
# blocs de decors venant du jeu : Broforce
# realise par : BUTAUD Valentin, BEREL Mehdi, CAMBIER Elliot, CARANGEOT Hugo
