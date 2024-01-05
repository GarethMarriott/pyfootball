from dataclasses import dataclass

@dataclass
class Player:
    """Player"""
    name: str

    # Physical
    Acceleration: int
    Speed: int
    Strength: int
    Agility: int
    Fitness: int

    # Mental
    Anticipation: int
    Composure: int
    Concentration: int
    Aggression: int
    Work_Rate: int

    # Technique
    Throw_Power: int
    Throw_Accuracy: int
    Pass_Vision: int
    Juking: int
    Catching: int
    Route_Running: int
    Run_Block: int
    Pass_Block: int
    Open_field_blocking: int
    Tackling: int
    Positioning_Run: int
    Positioning_Man: int
    Positioning_Zone: int
    Pass_Rush: int
    
    def get_name(self) -> str:
        return self.name