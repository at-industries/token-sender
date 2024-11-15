class Level:
    def __init__(self, name: str):
        self.name = name


DEB = Level(
    name='DEB',
)
INF = Level(
    name='INF',
)
WAR = Level(
    name='WAR',
)
ERR = Level(
    name='ERR',
)
FAT = Level(
    name='FAT',
)
LEVELS_DICT = {
    DEB.name: DEB,
    INF.name: INF,
    WAR.name: WAR,
    ERR.name: ERR,
    FAT.name: FAT,
}
LEVELS_LIST = list(LEVELS_DICT.values())
LEVELS_NAMES_LIST = list(LEVELS_DICT.keys())
