from copy import (
    deepcopy,
)

class Enchantment:
    """Class describing an enchantement object"""

    #https://minecraft.gamepedia.com/Anvil/Mechanics#Costs_for_combining_enchantments
    ENCHANTMENTS_DATA = {'Protection':{'maxLevel':4,'itemM':1,'bookM':1}, 'Fire Protection':{'maxLevel':4,'itemM':2,'bookM':1}, 'Feather Falling':{'maxLevel':4,'itemM':2,'bookM':1}, 'Blast Protection':{'maxLevel':4,'itemM':4,'bookM':2}, 'Projectile Protection':{'maxLevel':4,'itemM':2,'bookM':1}, 'Thorns':{'maxLevel':3,'itemM':8,'bookM':4}, 'Respiration':{'maxLevel':3,'itemM':4,'bookM':2}, 'Depth Strider':{'maxLevel':3,'itemM':4,'bookM':2}, 'Aqua Affinity':{'maxLevel':1,'itemM':4,'bookM':2}, 'Sharpness':{'maxLevel':5,'itemM':1,'bookM':1}, 'Smite':{'maxLevel':5,'itemM':2,'bookM':1}, 'Bane of Arthropods':{'maxLevel':5,'itemM':2,'bookM':1}, 'Knockback':{'maxLevel':2,'itemM':2,'bookM':1}, 'Fire Aspect':{'maxLevel':2,'itemM':4,'bookM':2}, 'Looting':{'maxLevel':3,'itemM':4,'bookM':2}, 'Efficiency':{'maxLevel':5,'itemM':1,'bookM':1}, 'Silk Touch':{'maxLevel':1,'itemM':8,'bookM':4}, 'Unbreaking':{'maxLevel':3,'itemM':2,'bookM':1}, 'Fortune':{'maxLevel':3,'itemM':4,'bookM':2}, 'Power':{'maxLevel':5,'itemM':1,'bookM':1}, 'Punch':{'maxLevel':2,'itemM':4,'bookM':2}, 'Flame':{'maxLevel':1,'itemM':4,'bookM':2}, 'Infinity':{'maxLevel':1,'itemM':8,'bookM':4}, 'Luck of the Sea':{'maxLevel':3,'itemM':4,'bookM':2}, 'Lure':{'maxLevel':3,'itemM':4,'bookM':2}, 'Frost Walker':{'maxLevel':2,'itemM':4,'bookM':2}, 'Mending':{'maxLevel':1,'itemM':4,'bookM':2}, 'Curse of Binding':{'maxLevel':1,'itemM':8,'bookM':4}, 'Curse of Vanishing':{'maxLevel':1,'itemM':8,'bookM':4}, 'Impaling':{'maxLevel':5,'itemM':4,'bookM':2}, 'Riptide':{'maxLevel':3,'itemM':4,'bookM':2}, 'Loyalty':{'maxLevel':3,'itemM':1,'bookM':1}, 'Channeling':{'maxLevel':1,'itemM':8,'bookM':4}, 'Multishot':{'maxLevel':1,'itemM':4,'bookM':2}, 'Piercing':{'maxLevel':4,'itemM':1,'bookM':1}, 'Quick Charge':{'maxLevel':3,'itemM':2,'bookM':1}, 'Sweeping Edge':{'maxLevel':3,'itemM':4,'bookM':2} }

    def __init__(self, name, level):
        """If level is not set, the maximum level is set instead. This is usefull for enchantments that has one level."""
        self.__name = name

        self.__maxLevel = Enchantment.ENCHANTMENTS_DATA[name]['maxLevel']
        self.__itemM = Enchantment.ENCHANTMENTS_DATA[name]['itemM']
        self.__bookM = Enchantment.ENCHANTMENTS_DATA[name]['bookM']

        if level == None:
            self.setLevel(self.__maxLevel)
        else
            self.setLevel(level)

    def name(self):
        return self.__name

    def level(self):
        return self.__level

    def maxLevel(self):
        return self.__maxLevel

    def itemM(self):
        return self.__itemM

    def bookM(self):
        return self.__bookM

    def setLevel(self, level):
        self.__level = level if level <= self.__maxLevel else self.__maxLevel

    def copy(self):
        return deepcopy(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name() == other.name() and self.level() == other.level()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        levelStr = 'I'
        if self.__level == 2: levelStr = 'II'
        elif self.__level == 3: levelStr = 'III'
        elif self.__level == 4: levelStr = 'IV'
        elif self.__level == 5: levelStr = 'V'

        return self.__name+' '+levelStr
