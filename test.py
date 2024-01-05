import random
import itertools
import numpy as np
import sys
import Player
from Plays import DefPlay,OffPlay,Playbook_def,Playbook_off,Play
from dataclasses import dataclass
from pprint import pp

def poisson_generator(lam, size=1000):
    """
    Generator function that yields values from a Poisson distribution.
    """
    while True:
        val = np.random.poisson(lam, size).tolist()
        while len(val) != 0:
            yield val.pop()

# Example usage
# poisson_gen = poisson_generator(lam=2, size=10)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



# OLD GAME TESTER
############################################################################
# class Game:
#     def __init__(self) -> None:
#         self.yards_to_first = 10
#         self.yards_to_TD = 100
#         self.down = 1

#     def reset(self):
#         self.yards_to_first = 10
#         self.yards_to_TD = 100
#         self.down = 1

#     def yards_result(self, yards):
#         if yards >= self.yards_to_TD:
#             self.reset()
#             return "TD"
#         else:
#             self.yards_to_TD -= yards
#             if yards >= self.yards_to_first:
#                 self.down = 1
#                 self.yards_to_first = 10
#                 return "First Down"
#             else:
#                 self.yards_to_first -= yards
#                 if self.down == 4:
#                     self.reset()
#                     return "Turnover"
#                 else:
#                     self.down += 1
#         return str(yards) + " yards gained"

#     def play_result(self,off_play,def_play):
#         return randint(1,6)

#     def drive(self , Playbook_off , Playbook_def):
#         result = ""
#         while True:
#             print("Down: "+str(self.down) + "  Yards_to_First_Down: " + str(self.yards_to_first) + "  Yards_to_TD: " + str(self.yards_to_TD))
#             off_play = Playbook_off.get()
#             def_play = Playbook_def.get()
#             result = self.yards_result(self.play_result(off_play,def_play))
#             print(result)
#             if result == "TD" or result == "Turnover":
#                 break

#########################################################################################


# SAMPLE PLAYERS
DB1 = Player.Player(name= "DB1",
    Acceleration = 9,
    Speed = 6,
    Strength = 6, 
    Agility = 7,
    Fitness = 8,
    Anticipation = 4,
    Composure = 5,
    Concentration = 5,
    Aggression = 8,
    Work_Rate = 9,
    Throw_Power = 1,
    Throw_Accuracy = 1,
    Pass_Vision = 1,
    Juking = 4,
    Catching = 7,
    Route_Running = 5,
    Run_Block = 1,
    Pass_Block = 1,
    Open_field_blocking = 2,
    Tackling = 8,
    Positioning_Run = 6,
    Positioning_Man = 8,
    Positioning_Zone = 7,
    Pass_Rush = 5
    )

WR1 = Player.Player(name= "WR1",
    Acceleration = 9,
    Speed = 7,
    Strength = 3, 
    Agility = 8,
    Fitness = 8,
    Anticipation = 8,
    Composure = 5,
    Concentration = 5,
    Aggression = 4,
    Work_Rate = 9,
    Throw_Power = 1,
    Throw_Accuracy = 1,
    Pass_Vision = 1,
    Juking = 7,
    Catching = 7,
    Route_Running = 8,
    Run_Block = 4,
    Pass_Block = 4,
    Open_field_blocking = 4,
    Tackling = 2,
    Positioning_Run = 1,
    Positioning_Man = 2,
    Positioning_Zone = 3,
    Pass_Rush = 1
    )

QB1 = Player.Player(name= "QB1",
    Acceleration = 5,
    Speed = 5,
    Strength = 6, 
    Agility = 7,
    Fitness = 8,
    Anticipation = 4,
    Composure = 5,
    Concentration = 5,
    Aggression = 8,
    Work_Rate = 9,
    Throw_Power = 9,
    Throw_Accuracy = 7,
    Pass_Vision = 8,
    Juking = 3,
    Catching = 2,
    Route_Running = 2,
    Run_Block = 1,
    Pass_Block = 1,
    Open_field_blocking = 2,
    Tackling = 2,
    Positioning_Run = 3,
    Positioning_Man = 3,
    Positioning_Zone = 2,
    Pass_Rush = 1
    )

#######################################



def resolve_coverage_zone(play_segment,WR:Player,DBs:list):
    """ 
    Input: 
        play_segment: TODO implement extra details about play segment such as ?previous routes modifier? TBD
        WR: Player Class with player in coverage zone
        DBs: List of DBs in current coverage zone

    Usage:
        Determine ahead of time the recievers and DBs in a coverage zone and baised off of Player stats determine how open they are.
        
        TODO implement DBs using zone coverage stat when in zone not always using Man coverage stat
        TODO rethink sim alg, is there a better way to determine if a reciever is open
        TODO Add a modifier if the reciever is on the second part of a route to make his chance of being open better if he beat the DB on the first part of the route

    Output:
        Percentage the reciever is open
    """
    # Physical Battle
    WR_physical_stat = (4*WR.Acceleration) + (3*WR.Speed) + (1*WR.Strength) + (2*WR.Agility)
    DBs_physical_stats = list(map(lambda x: (4*x.Agility) + (2*x.Strength) + (2*x.Speed) + (2*x.Acceleration), DBs))

    WR_phys_roll = np.random.poisson(WR_physical_stat, 1)[0]
    DB_phys_roll = max(list(map(lambda x: np.random.poisson(x, 1)[0], DBs_physical_stats)))
    
    Physical_Battle_Modifier = WR_phys_roll - DB_phys_roll

    # print(f'Num of DBs = {len(DBs)}')
    
    # print(f'WR phys stat {WR_physical_stat}')
    # print(f'WR phys roll {WR_phys_roll}')

    # print(f'DB Phys stat {DBs_physical_stats}')
    # print(f'DB Phys roll {DB_phys_roll}')
    
    # print(f'Physical Battle result {Physical_Battle_Modifier}')
    
    # if Physical_Battle_Modifier >= 0:
    #     print(f"WR won Physical battle\n")
    # else:
    #     print(f"DB won Physical battle\n")


    # Tecnique Battle
    WR_tec_stat = (7*WR.Route_Running) + (3*WR.Catching)
    
    DB_tec_stats = list(map(lambda x: (10*x.Positioning_Man), DBs))

    WR_tec_roll = np.random.poisson(WR_tec_stat, 1)[0]
    DB_tec_roll = max(list(map(lambda x: np.random.poisson(x, 1)[0], DB_tec_stats)))

    # print(f'WR tec stat {WR_tec_stat}')
    # print(f'WR tec roll {WR_tec_roll}')

    # print(f'DB tec stat {DB_tec_stats}')
    # print(f'DB tec roll {DB_tec_roll}')

    Tec_Battle_Modifier = WR_tec_roll - DB_tec_roll
    
    # if Tec_Battle_Modifier >= 0:
    #     print("WR won Tecnical battle")
    # else:
    #     print("DB won Tecnical battle")

    coverage_percent = (3 + Physical_Battle_Modifier + Tec_Battle_Modifier) / 10

    # if coverage_percent > 0:
    #     print(f'{bcolors.OKCYAN}The Receiver is {coverage_percent*10:.2f}% open{bcolors.ENDC}')
    # else:
    #     print(f'{bcolors.OKGREEN}The Receiver is {coverage_percent*10:.2f}% open{bcolors.ENDC}')

    return coverage_percent

def attempt_pass(openness, play_segment, QB:Player, DBs:list):
    print(openness)
    QB_pass_stat = (float(QB.Throw_Accuracy*0.7)+float(QB.Throw_Power*0.3))*(openness/5)
    QB_pass_roll = np.random.poisson(QB_pass_stat, 1)[0]

    DB_tec_stats = list(map(lambda x: (x.Anticipation), DBs))
    DB_tec_roll = max(list(map(lambda x: np.random.poisson(x, 1)[0], DB_tec_stats)))

    # print(f'QB pass stat {QB_pass_stat}')
    print(f'QB pass roll {QB_pass_roll}')

    # print(f'DB tec stat {DB_tec_stats}')
    print(f'DB tec roll {DB_tec_roll}')

    if QB_pass_roll > DB_tec_roll:
        return f"gain of {random.randint(1,30)}"
    else:
        return "Incomplete"


def qb_pick_pass(recievers:dict, QB:Player):
    # pp(recievers)
    # print(f"QB pass stat {QB.Pass_Vision}")

    for key,value in sorted(recievers.items(), key=lambda x: x[1], reverse=True):
        if value < 0:
            pass
        QB_pass_roll = (value/10)*(np.random.poisson(QB.Pass_Vision, 1)[0])/10
        print(f"QB pass roll {QB_pass_roll}")
        
        rand_chance = random.random()
        print(f"random chance {rand_chance}")

        if QB_pass_roll >= rand_chance:
            return {key:value}


# TODO implement RUN plays
def resolve_play(current_play:Play):
    # off_play = play.off_play
    # def_play = play.def_play
    if current_play.off_play.play_call == "pass":
        return resolve_pass(current_play)



# TODO Implement QB decisions on who to pass to
# TODO Implement a way of managing players on a team
def resolve_pass(current_play:Play):
    off_play = current_play.off_play
    def_play = current_play.def_play

    # TODO assign man coverage in a smarter way
    # ASSIGN MAN COVERAGE
    # num in man = LB + DB - Num in zone - num blitzing
    num_in_man_cov = def_play.formation[1] + def_play.formation[2] - len(def_play.zones) - def_play.blitz
    current_play.coverage_zones = def_play.zones
    for i in range(0,num_in_man_cov):
        current_play.coverage_zones.append(off_play.routes[i])

       
    # SIM PASS
    for read_num in range(0,2):
        # print(read_num)
        current_play.recievers = dict()
        for route in off_play.routes:
            what_zone = route[read_num]
            DBs_in_zone_coverages = list(filter(lambda x: what_zone in x, current_play.coverage_zones))
            DBs_in_zone = []
            for i in range(0,len(DBs_in_zone_coverages)):
                DBs_in_zone.append(DB1)


            # print(f'\n\nResolve coverage in zone {what_zone}')
            current_play.recievers[what_zone] = resolve_coverage_zone("placeholder", WR1, DBs_in_zone)
        
        # print(recievers)
        pass_attempt = qb_pick_pass(current_play.recievers,QB1) # TODO implement using proper QB not default
        if pass_attempt != None:
            current_play.what_zone_attempted_pass = list(pass_attempt.keys())[0]
            DBs_in_zone_coverages = list(filter(lambda x: current_play.what_zone_attempted_pass in x, current_play.coverage_zones))
            DBs_in_zone = []
            for i in range(0,len(DBs_in_zone_coverages)):
                DBs_in_zone.append(DB1)
            pass_result = attempt_pass(current_play.recievers[current_play.what_zone_attempted_pass],"to_be_implemented",QB1,DBs_in_zone)
            return pass_result

    print("No pass")
    scramble_yards = random.randint(-10,20)
    if scramble_yards >= 0:
        return f"Scrabled for {scramble_yards} yards" 
    else:
        return f"Sacked. Loss of {abs(scramble_yards)}"


# def one_on_one_coverage_test(QB,WR,DB):
#     coverage_percent = resolve_coverage("Man-Coverage-Deep-Corner",WR,DB)

def_playbook1 = Playbook_def()
def_playbook1.plays.append(DefPlay(5,2,4,0,[[1,2],[4,5]]))
pp(def_playbook1)

off_playbook1 = Playbook_off()
off_playbook1.plays.append(OffPlay("pass",(1,1),[[6,1],[10,5],[7,8],[9,10],[12,12]]))
pp(off_playbook1)

print(resolve_play(Play(name="tester",off_play=off_playbook1.plays[0],def_play=def_playbook1.plays[0])))

# x = []
# for i in range(0,10000):
#     print(i,end="\r")
#     x = x + resolve_play(off_playbook1.plays[0],def_playbook1.plays[0])

# pp(x)
# pp(min(x))
# pp(max(x))
# pp(sum(x)/len(x))


# one_on_one_coverage_test(QB1,WR1,DB1)