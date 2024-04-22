from pygame import *
from random import randint
from time import time as timer



#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#шрифты и надписи
font.init()
font1 = font.Font("Arial", 100)
win = font1.render('YOU WIN', True,(255,255,255))
lose = font1.render('YOU DIED', True,(180,0,0))

font2 = font.Font("Arial", 36)


#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = 'bullet.png' #пуля
img_asteroid = 'asteroid.png'

font1 = font.Font("Arial", 64)
lost = font1.render('YOU LOSE!', True, (255,255,255))

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
goal = 30 #количество убитых противников
max_lost = 3 #количество пропусков


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       #метод выстрел, используем место игрока, чтобы создать там пулю
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

#класс спрайта-врага
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #если дойдет до края экрана, то исчезает
        if self.rect.y < 0:
            self.kill()
#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
rel_time = False #флаг, отвечающий за перезарядку
num_fire = 0 #переменная для подсчета выстрелов

while run:
   #событие нажатия на кнопку “Закрыть”
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                   num_fire = num_fire + 1
                   ship.fire()
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


   if not finish:
       #обновляем фон
       window.blit(background,(0,0))
       #проверка столкновения пули и монстра (и монстр, и пуля - исчезают)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       # этот цикл повторяется столько раз, соклько монстров подбито
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       #возможный проигрыш: пропустили слишком много врагов или столкнулись с ними
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
           finish = True #проиграли
           window.blit(lose, (200, 200))
       #проверка выигрыша: сколько очков набрали?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))



       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))


       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()

       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       

        #перезарядка
        if rel_time == True:
            now_time = timer() #считываем время

            
                   
          
    
     else:   
          num_fire = 0 #обнуляем счетчик пуль
          rel_time = False #сбрасываем флаг перезарядки
 display.update()      
        finish = False
        score = 0 
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(5000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        

   #цикл срабатывает каждую 0.05 секунд
   time.delay(50)
