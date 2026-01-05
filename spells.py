class Spell:
    def __init__(self, spellName, costMP):
        self.spellName = spellName
        self.costMP = costMP

class MageSpell(Spell):
    def __init__(self, spellName, costMP, dmg):
        super().__init__(spellName, costMP)
        self.dmg = dmg

class HealSpell(Spell):
    def __init__(self, spellName, costMP, heal):
        super().__init__(spellName, costMP)
        self.heal = heal

class Spells:
    def __init__(self):
        self.mageSpells: dict[str, MageSpell]={}
        self.healSpells: dict[str, HealSpell]={}
    
    def addMageSpell(self, mageSpell: MageSpell):
        self.mageSpells[mageSpell.spellName] = mageSpell

    def addHealSpell(self, healSpell: HealSpell):
        self.healSpells[healSpell.spellName] = healSpell


mageSpells = {
    "fireball": MageSpell("fireball", 60, 40),
    "scorch": MageSpell("scorch", 30, 20)
}

healSpells = {
    "greatHeal": HealSpell("greatHeal", 60, 80),
    "heal": HealSpell("heal", 30, 40),
    "massHeal": HealSpell("massHeal", 45, 35)
}

spells = Spells()
for i in mageSpells:
    spells.addMageSpell(mageSpells[i])

for i in healSpells:
    spells.addHealSpell(healSpells[i])

