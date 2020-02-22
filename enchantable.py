from copy import (
    deepcopy,
)

from .utils import (
    p,
)

from .enchantment import (
    Enchantment,
)


class EnchantableItem:
    def __init__(self, enchantments=[], name="Item", pwp=0):
        self.__name = name
        self.__pwp = pwp #prior work penalty
        self.__enchantments = {}
        self._isBook = False

        for enchantment in enchantments:
            if enchantment.name() in self.__enchantments:
                raise Exception(self.__class__.__name__+"("+name+") initialization has failed: Duplicated enchantement: " + str(enchantment))
            self.__enchantments[enchantment.name()] = enchantment.copy()

    def copy(self):
        return deepcopy(self)

    def rename(self, newName):
        if newName and self.__name != newName:
            self.__name = newName
            return True
        else:
            return False

    def addEnchantments(self, enchantedItem, simulate=False):
        xpCost = 0
        multiplier = 'bookM' if enchantedItem.isBook() else 'itemM'

        for enchantment in enchantedItem.enchantments():
            enchentmentLevel = enchantment.level()
            if(enchantment.name() not in self.__enchantments):
                if not simulate:
                    self.__enchantments[enchantment.name()] = enchantment.copy()
            else:
                oldEnchamtment = self.__enchantments[enchantment.name()]
                if oldEnchamtment.level() > enchantment.level():
                    enchentmentLevel = oldEnchamtment.level()
                elif oldEnchamtment.level() == enchantment.level():
                    enchentmentLevel += 1

                if not simulate:
                    oldEnchamtment.setLevel(enchentmentLevel)

            xpCost += Enchantment.ENCHANTMENTS_DATA[enchantment.name()][multiplier]*enchentmentLevel

        return xpCost


    def enchantments(self):
        return list(self.__enchantments.values())

    def clearEnchantments(self):
        self.__pwp = 0
        self.__enchantments.clear()

    def name(self):
        return self.__name

    def isBook(self):
        return self._isBook

    def setPWP(self, pwp):
        self.__pwp = pwp

    def pwp(self):
        return self.__pwp

    def pwpCost(self):
        return p(self.__pwp)

    def echtCost(self):
        multiplier = 'bookM' if self._isBook else 'itemM'

        return sum([ Enchantment.ENCHANTMENTS_DATA[enchantment.name()][multiplier]*enchantment.level() for enchantment in self.__enchantments.values() ])

    def __and__(self, other):
        """Returns self if self is contained in other, or other if it's contained in self"""
        """Ex: if self=Book(Fire Aspect I) and other=Book(Fire Aspect II, Unbreaking III) then, self&other=self"""

        sn, on = len(self.enchantments()), len(other.enchantments())
        bigger, smaller = None, None

        if sn > on:
            bigger, smaller = self, other
        else:
            bigger, smaller = other, self

        biggerEchts = bigger.enchantments()

        for se in smaller.enchantments():
            duplicated = False
            for be in biggerEchts:
                if be.name() == se.name() and (be.level() > se.level() or be.level() == se.level() == se.maxLevel()):
                    duplicated = True
                    break
            if not duplicated:
                return None

        return smaller


    def __repr__(self):
        return self.__str__()

    def __str__(self):

        if self._isBook and self._isFromTwoBooks:
            return self.__name + '('+ str(self._isFromTwoBooks[0]) + '+' + str(self._isFromTwoBooks[1]) + ',' + str(self._isFromTwoBooks[2]) + ')'

        enchamtmentsStr = ', '.join([ enchantment.__str__() for enchantment in self.__enchantments.values() ])
        if enchamtmentsStr:
            return self.__name+'('+enchamtmentsStr+')'
        else:
            return self.__name


class EnchantedBook(EnchantableItem):
    def __init__(self, enchantments=[]):
        super().__init__(enchantments)
        self._isBook = True
        self._isFromTwoBooks = False
        self.rename("Book")

    def fromBooks(self,b1,b2):
        if self._isFromTwoBooks:
            return False

        self.addEnchantments(b1)

        xpCost = self.addEnchantments(b2)+b1.pwpCost()+b2.pwpCost()

        self.setPWP(max(b1.pwp(),b2.pwp())+1)
        self._isFromTwoBooks = (b1,b2,xpCost)

        return xpCost
