from .utils import (
    p,
)

from .enchantment import (
    Enchantment,
)

from .enchantable import (
    EnchantableItem,
    EnchantedBook,
)

TOO_EXPENSIVE = "Too expensive !"

def AnvilSimulator(target, sacrifice, newName=''):
    #https://minecraft.gamepedia.com/Anvil/Mechanics#Combining_items
    """Simulates anvil mechanics"""
    """sacrifice can be NULL if setting the target name"""

    #Repairing is not yet supported

    xpCost = None

    if(sacrifice == None and newName):
        if target.rename(newName):
            xpCost = target.pwp()+1
    elif sacrifice != None:
        xpCost = target.pwpCost()+sacrifice.pwpCost()

        if target.rename(newName):
            xpCost += 1

        xpCost += target.addEnchantments(sacrifice)

        target.setPWP(max(target.pwp(), sacrifice.pwp())+1)

    return xpCost

def removeDuplicatedEnchantments(enchantedItems):
    """Removes duplicates from enchantedItems and returns them separately"""
    """Exemple1: [Book(Fire Aspect I), Book(Fire Aspect II, Unbreaking III)] becomes [Book(Fire Aspect II, Unbreaking III)]"""
    """Exemple2: [Book(Fire Aspect I), Book(Fire Aspect I, Unbreaking III)] stay unchanged"""

    n = len(enchantedItems)
    duplicates = ()

    for i in range(n):
        for j in range(i+1, n):
            #see & operator implementation in EnchantableItem class
            duplicate = enchantedItems[i] & enchantedItems[j]
            if duplicate != None:
                duplicates += (duplicate,)

    clearedList = list(enchantedItems)
    for duplicate in duplicates:
        clearedList.remove(duplicate)

    return clearedList, duplicates

def sortEnchantableItemsByPWP(enchantableItems):
    """Sorts ascending all items in enchantableItems by their pwp (prior work penalty) and returns them in a new list."""
    """If two items have the same pwp then they're sorted by their echtCost."""
    n = len(enchantableItems)
    if n <= 1:
        return enchantableItems
    else:
        e0, l1, l2 = enchantableItems[0], [], []
        for i in range(1, n):
            #If pwp are equal sort by echtCost
            if enchantableItems[i].pwp() < e0.pwp() or (enchantableItems[i].pwp() == e0.pwp() and enchantableItems[i].echtCost() < e0.echtCost()):
                l1 += [enchantableItems[i]]
            else:
                l2 += [enchantableItems[i]]

        return sortEnchantableItemsByPWP(l1)+[e0]+sortEnchantableItemsByPWP(l2)

def BasicBooksEnchantingXPCosts(target, sortedBooks):
    """Returns a list of XP costs of each operation: book applied to target."""
    """Returns [] if one of the elementary operations cost exceeds 39 levels."""
    cTarget = target.copy()
    costs = []
    for i in range(len(sortedBooks)):
        xpCost = cTarget.addEnchantments(sortedBooks[i])+sortedBooks[i].pwpCost()+cTarget.pwpCost()
        if xpCost >= 40:
            return []

        costs += [xpCost]
        cTarget.setPWP(max(cTarget.pwp(), sortedBooks[i].pwp())+1)

    return costs

def BasicBooksEnchantingXPCost(target, sortedBooks):
    return sum(BasicBooksEnchantingXPCosts(target, sortedBooks))

def BestBooksEnchantmentCombination(target, books, previousCost=0):
    """Finds the best combination in terms of XP Cost, and return a list [TotalXPCost, combinations] where combinations is a recursive tuple including all the combinations with their elementary costs"""
    """It returns TOO_EXPENSIVE in case there is no possible combinations in Survival Mode (one of the elementary costs exceeds 39 levels)"""

    """previousCost\n
            This parameter is reserved and must be 0"""
    n = len(books)

    # Get a shallow copy of books
    sortedBooks = list(books)

    # previousCost is not 0 only when called programmatically (see recusive calls of this function below)
    # and in a recursive call books is already sorted.
    if previousCost==0:
        sortedBooks = sortEnchantableItemsByPWP(books)

    basicXPCosts = BasicBooksEnchantingXPCosts(target, sortedBooks)
    basicXPCost = sum(basicXPCosts)
    # basicXPCost can be 0 if one of the elementary costs exceeds 39 levels.
    if basicXPCost:
        basicXPCost += previousCost

    if n==1:
        if basicXPCost:
            return [basicXPCost, (target, books[0], basicXPCost)]
        else: #unfortunately it's TOO_EXPENSIVE
            return TOO_EXPENSIVE

    # All the math below is based on the anvil mechanics described here: https://minecraft.gamepedia.com/Tutorials/Anvil_mechanics
    elif n==2:
        b1,b2 = sortedBooks
        # b1 must have the higher echtCost
        if b1.echtCost() < b2.echtCost():
            b1,b2 = b2,b1

        combBook = EnchantedBook()
        combBooksCost = combBook.fromBooks(b1,b2)
        combItemBoosCost = target.addEnchantments(combBook, True)+target.pwpCost()+combBook.pwpCost()
        combXPCost = combBooksCost+combItemBoosCost

        if basicXPCost and combXPCost > basicXPCost:
            return [basicXPCost, ((target, b1, basicXPCosts[0]), (target, b2, basicXPCosts[1]))]

        # combXPCost will be the sum of two elementary operations, each one must be inferior at 39 levels
        # 78 = 39 + 39
        elif combXPCost <= 78:
            return [combXPCost, (target, (b1, b2, combBooksCost), combItemBoosCost)]
        # Unfortunately it's TOO_EXPENSIVE
        else:
            TOO_EXPENSIVE
    else:
        # This part is inspired by the 3 books case: Recurrence
        def Combine2BooksCost(b1,b2):
            return b1.addEnchantments(b2, True)+p(max(b1.pwp(),b2.pwp())+1)

        b1, b2 = sortedBooks[0], sortedBooks[1]
        minCost = Combine2BooksCost(b1,b2)

        # b1,b2 must give the minimum Combine2BooksCost(b1,b2)

        for i in range(n):
            for j in range(n):
                if j == i:
                    continue

                bi, bj = sortedBooks[i], sortedBooks[j]
                newCost = Combine2BooksCost(bi,bj)
                if newCost < minCost:
                    minCost = newCost
                    b1, b2 = bi, bj

        # Now Combine2BooksCost(b1,b2) = min( [ Combine2BooksCost(bi,bj) for i in range(n) for j in range(n) ] )
        sortedBooks.remove(b1)
        sortedBooks.remove(b2)
        n -= 2

        # Combine them in one book
        combBook = EnchantedBook()
        combXpCost = combBook.fromBooks(b1,b2)

        # Insert the combBook in sortedBooks and keep it sorted. See line 71
        combBookIdx = -1
        for i in range(n-1,-1,-1):
            if combBook.pwp() > sortedBooks[i].pwp() or (combBook.pwp() == sortedBooks[i].pwp() and combBook.echtCost() > sortedBooks[i].echtCost()):
                combBookIdx = i+1
                break

        if combBookIdx > -1:
            sortedBooks.insert(combBookIdx, combBook)
        else:
            sortedBooks.insert(0, combBook)

        # Now we compare between the costs of the basic combination and the advanced one
        # We don't forget to pass the combXpCost and the previousCost
        recursiveCombinationResult = BestBooksEnchantmentCombination(target, sortedBooks, combXpCost+previousCost)

        if recursiveCombinationResult == TOO_EXPENSIVE and not basicXPCost:
            return TOO_EXPENSIVE
        elif basicXPCost and basicXPCost < recursiveCombinationResult[0]:
            return [basicXPCost, tuple((target, books[i], basicXPCosts[i]) for i in range(n+2))]
        else:
            return recursiveCombinationResult
