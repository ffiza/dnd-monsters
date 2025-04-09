class Config:
    def __init__(self):
        self.CHALLENGE_RATINGS = [
            "0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10", "11", "12", "13", "14",
            "15", "16", "17", "18", "19", "20", "21", "22", "23",
            "24", "25", "26", "27", "28", "29", "30"]
        self.MONSTER_TYPES = [
            "Aberration", "Beast", "Celestial", "Construct", "Dragon",
            "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity",
            "Ooze", "Plant", "Undead"]
        self.SIZES = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
        self.ABILITIES = ["Strength", "Dexterity", "Constitution",
                          "Intelligence", "Wisdom", "Charisma"]
        self.FONT_STACK = (
            '-system-ui, -apple-system, BlinkMacSystemFont, '
            'Segoe UI", Roboto, Helvetica, Arial, sans-serif, '
            '"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"')
        self.WIDTH = 1400
