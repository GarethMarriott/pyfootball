from dataclasses import dataclass
from Player import Player
from pprint import pp


@dataclass
class Playbook_off:
    plays: list
    def __init__(self) -> None:
        self.plays = []
    
    def get_plays(self):
        return plays

@dataclass
class Playbook_def:
    plays: list
    def __init__(self) -> None:
        self.plays = []
    
    def get_plays(self):
        return plays


# TODO add players as part of data class
@dataclass
class DefPlay():
    formation: tuple
    blitz: int
    zones: list
    def __init__(self,DB_num,LB_num,DL_num,blitz,zones) -> None:
        super().__init__()
        self.formation = (DL_num,LB_num,DB_num)
        self.blitz = blitz # num of LB rushing QB
        self.zones = zones # List with each player haveing a sublist of zones they cover Eg. cover2 man under would have [[1,2],[4,5]] First Player covering zones 1 and 2 with second player covering zones 4 and 5


# TODO add players as part of data class
@dataclass
class OffPlay():
    play_call: str
    formation: tuple
    routes: list 
    def __init__(self,playcall,formation,routes) -> None:
        super().__init__()
        self.play_call = playcall # Pass | Run
        self.formation = formation # I formation(2,2,1) | Twins(2,2,1) | Twins(2,1,2) | Ace(3,1,1) | Trips(3,1,1) | Trips(2,1,2) | Empty(4,1,0) | Quads(4,1,0) | Bunch(3,1,1) 
        self.routes = routes # List with each player having sublist of zones they enter at each read. Eg. 4 verts [[6,1],[7,2],[9,4],[10,5]]
        # https://throwdeeppublishing.com/blogs/football-glossary/the-complete-guide-to-offensive-football-formations

@dataclass
class Play:
    name: str
    off_play: OffPlay
    def_play: DefPlay
    coverage_zones = []
    