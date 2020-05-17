# Minecraft-Enchantments-Master (MEM)

## Description
**Minecraft-Enchantments-Master** or **MEM** is a simple python program that simulates the enchantment mechanics of the anvil in the popular game: [Minecraft](https://fr.wikipedia.org/wiki/Minecraft).
It's based on the Official Minecraft Wiki page: [*Anvil/Mechanics*](https://minecraft.gamepedia.com/Anvil/Mechanics).

## Motivation
Let's say that you wanted a powerfull axe with all of the following enchantements: Sharpness V, Efficiency V, Silk Touch and Unbreaking III. Suppose that you got all corresponding enchanted books and you applied them one after the other to the axe using an anvil. You'll end up with a total cost of **28 EXP**.
But if you combined Silk Touch I and Unbreaking III first, and then you applied the rest of books then it will cost you **25 EXP**. 
This motivated me to write this program that by giving it the enchanted books you have, and the desired enchanted item, it gives you the cheapest (possible) books combination.

## Features
- [x] Calculate the exact total experience cost of any enchantment.
- [x] Find the minimum experience cost for a specific enchantements combination using enchanted books only.
- [ ] Find the minimum experience cost for a specific enchantements combination using enchanted books and items.
- [ ] Support items durability.

## Instalation


## Example
Let's take the example used in [Motivation](#Motivation)
```python
from mc-enchanter import *

axe = EnchantableItem([], "axe")

unbreaking3 = EnchantedBook([ Enchantment('Unbreaking', 3) ])
sharpness5 = EnchantedBook([ Enchantment('Sharpness', 5) ])
efficiency5 = EnchantedBook([ Enchantment('Efficiency', 5) ])
silk_touch = EnchantedBook([ Enchantment('Silk Touch', 1) ])

enchantedBooks = [unbreaking3, sharpness5, efficiency5, silk_touch]
combination = BestBooksEnchantmentCombination(axe, enchantedBooks)

print(combination)
```
Output
```
[25, ((axe, Book(Sharpness V), 5), (axe, Book(Efficiency V), 6), (axe, Book(Book(Silk Touch I)+Book(Unbreaking III),3), 11))]
 ^ The    | ^_> Combine the axe    |  ^_> Combine the axe       |    ^_> 1- Combine Book(Silk Touch I) with Book(Unbreaking III) costs 3 EXP
 cheapest | with Book(Sharpness V) |  with Book(Efficiency V)   |     2- Combine axe with the resulting book: Book(Book(Silk Touch I)+Book(Unbreaking III),3)
   cost   |     costs 5 EXP        |      costs 6 EXP           |                            costs 11 EXP
```

