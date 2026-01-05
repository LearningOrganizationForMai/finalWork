from character import Characteristics
from classes import Archer, Healer, Mage, Warrior
from weapon import weapons
from armor import armors
import globals

aragorn = Warrior('Aragorn', 
                  weapons.warrior.swords["exscalibur"], 
                  armors.warrior["fullplate"])

legolas = Archer('Legolas', 
                 weapons.archer.bows["galadhrim"], 
                 armors.archer["leather"])

abaddon = Mage('Abaddon', 
               weapons.mage.staffs["mysticStaff"], 
               armors.mage["robe"])

chen = Healer('Chen', 
            weapons.mage.staffs["staffOfWizardry"], 
            armors.healer["chainmail"])


defaultParty = [aragorn, legolas, abaddon, chen]


def createPartyFromSave(party, classMap=globals.CLASS_MAP):
    new_party = []
    for char in party:
        className = char["className"].lower()
        weaponClass = char["weapon"]["weaponClass"]
        weaponName = char["weapon"]["weaponName"]
        weapon = getattr(
            getattr(weapons, className),
            weaponClass
        )[weaponName]
        armor = getattr(armors, className)[char["armor"]]
        loadedCharacter = classMap[char["className"]](
            name=char["name"], 
            weapon=weapon, 
            armor=armor, 
            characteristics=mapCharacteristics(char)
            )
        loadedCharacter.loadArtifacts(char["artifacts"])
        new_party.append(loadedCharacter)
    return new_party


def mapCharacteristics(data):
    return Characteristics(
        HP=data["HP"], 
        MP=data["MP"], 
        strength=data["strength"], 
        dexterity=data["dexterity"], 
        intelligence=data["intelligence"])


def getArtifacts(party):
    artifacts = []
    for char in party:
        artifacts.append(char.showArtifacts())
    return artifacts

