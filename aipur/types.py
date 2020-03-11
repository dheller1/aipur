import colorama
import enum


class Player(enum.Enum):
    Alex = 1
    Bill = 2

    def __str__(self):
        if self == Player.Alex:
            return 'Alex'
        elif self == Player.Bill:
            return 'Bill'


class Goods(enum.Enum):
    Leather = 1
    Spices = 2
    Cloth = 3
    Silver = 4
    Gold = 5
    Diamonds = 6
    Camel = 7

    def __str__(self):
        if self == Goods.Leather:
            return colorama.Fore.YELLOW + '[L]' + colorama.Style.RESET_ALL
        elif self == Goods.Spices:
            return colorama.Fore.GREEN + '[S]' + colorama.Style.RESET_ALL
        elif self == Goods.Cloth:
            return colorama.Fore.MAGENTA + '[C]' + colorama.Style.RESET_ALL
        elif self == Goods.Silver:
            return colorama.Fore.WHITE + colorama.Style.BRIGHT + '[S]' + colorama.Style.RESET_ALL
        elif self == Goods.Gold:
            return colorama.Fore.YELLOW + colorama.Style.BRIGHT + '[G]' + colorama.Style.RESET_ALL
        elif self == Goods.Diamonds:
            return colorama.Fore.RED + colorama.Style.BRIGHT + '[D]' + colorama.Style.RESET_ALL
        elif self == Goods.Camel:
            return colorama.Fore.YELLOW + 'Cam' + colorama.Style.RESET_ALL

class BonusTiles(enum.Enum):
    Three = 3
    Four = 4
    Five = 5
