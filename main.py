import random
from health_error import HealthError
from mood_error import MoodError
from money_error import MoneyError
from action import Action
from work import Work
from rest import Rest


class Person:
    def __init__(self, name, health=0, mood=0, money=0):
        self.name = name
        self.health = health
        self.mood = mood
        self.money = money
        self.action = None

    def __str__(self):
        action_info = f' (Действие: {self.action.name})' if self.action else ''
        return f'~~~ {self.name} ~~~\nСостояние здоровья: {self.health}\nНастроение: {self.mood}\nБаланс: {self.money}{action_info}'

    def change_state(self, health=0, mood=0, money=0):
        if self.health + health < 0:
            raise HealthError("Мемолорд пал смертью храбрых")
        if self.mood + mood < 0:
            raise MoodError("Мемолорд впал в дипрешн")
        if self.money + money < 0:
            raise MoneyError("Мемолорд обанкротился")

        self.health += health
        self.mood += mood
        self.money += money

        if self.health >= 100 and self.mood >= 100:
            print(f"{self.name} выиграл! Поздравляем!")
            exit()
        elif self.health <= 0:
            print(f"{self.name} проиграл... Мемолорд умер.")
            exit()

    def do(self, action):
        self.action = action
        if isinstance(action, Work):
            if self.mood > 90:
                self.change_state(action.health, action.mood, action.money * 1.1)
            else:
                self.change_state(action.health, action.mood, action.money)
        elif isinstance(action, Rest):
            if self.health < 40:
                self.change_state(action.health, int(action.mood * 0.8), action.money)
            else:
                self.change_state(action.health, action.mood, action.money)
        elif isinstance(action, Action):
            self.change_state(action.health, action.mood, action.money)


ment = Person(name='Мент', money=random.randint(0, 100), mood=random.randint(0, 100), health=random.randint(50, 100))

meme_lords = [
    Person(name='Анимешница', money=random.randint(0, 100), mood=random.randint(0, 100),
           health=random.randint(50, 100)),
    Person(name='Собака', money=random.randint(0, 100), mood=random.randint(0, 100), health=random.randint(50, 100))
]

actions = [
    Work(name='пойти работать сварщиком', money=50, mood=-10, health=-3),
    Rest(name='Полежать', money=0, mood=15, health=0),
    Action(name='Подумать о жизни', health=2, mood=-5, money=0),
    Action(name='Поиграть в Бравл Старс', health=-3, mood=10, money=0),
    Rest(name='Сходить в больничку', money=-30, mood=-10, health=5)
]

print("Стартовые статы персонажей:")
print(ment)
for meme_lord in meme_lords:
    print(meme_lord)
print("-" * 30)


def choose_action(meme_lord):
    print(f"Выбери действие для Мента:")
    print("1. Пойти работать сварщиком(дает: денег:50, настроение:-10, здоровье:-3)")
    print("2. Полежать(дает: денег:-8, настроение:15, здоровье:0)")
    print("3. Подумать о жизни(дает: денег:0, настроение:-5, здоровье:2)")
    print("4. Поиграть в Бравл Старс(дает: денег:0, настроение:10, здоровье:-3)")
    print("5. Сходить в больничку(дает: денег:-30, настроение:-10, здоровье:5)")

    print(f"Текущие статы: Здоровье: {meme_lord.health}, Настроение: {meme_lord.mood}, Деньги: {meme_lord.money}")

    choice = input("Написать номер действия: ")
    if choice.isdigit() and 1 <= int(choice) <= 5:
        return actions[int(choice) - 1]
    else:
        print("Некорректный ввод. Пожалуйста, введите число от 1 до 5.")
        return choose_action(meme_lord)


while len(meme_lords) > 0:
    player_action = choose_action(ment)
    bot_actions = [random.choice(actions) for _ in range(len(meme_lords))]

    try:
        ment.do(player_action)
        print(ment)
    except (HealthError, MoodError, MoneyError) as e:
        print(f"Ой-ой: {e}. {ment.name} проиграл... он умер.")
        exit()

    for i, meme_lord in enumerate(meme_lords):
        try:
            action = bot_actions[i]
            meme_lord.do(action)
            print(meme_lord)
        except (HealthError, MoodError, MoneyError) as e:
            print(f"Ой-ой: {e}. {meme_lord.name} удалён из списка.(переиграл в Бравл Старс.. наверное)")
            meme_lords.remove(meme_lord)
    print