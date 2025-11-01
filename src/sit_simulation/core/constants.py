from enum import StrEnum

class StateNames(StrEnum):
    EGG = "Egg"
    LARVA = "Larva"
    PUPA = "Pupa"
    WM = "WildMale"
    SM = "SterileMale"
    YF = "YoungFemale"
    FF = "FertileFemale"
    MF = "MatedFemale"
    SF = "SterileFemale"
    DEAD = "Dead"

ADULT_STATES = [
    StateNames.WM,
    StateNames.SM,
    StateNames.YF,
    StateNames.FF,
    StateNames.MF,
    StateNames.SF
]

class InsectTypes(StrEnum):
    Sterile = "SterileInsect"
    Wild = "WildInsect"

class ProbabilityDistribution(StrEnum):
    UNIFORM = "uniform"
    GEOM = "geom"
    NORMAL = "norm"
    WEIBULL = "weibull"
    BERNOULLI = "bernoulli"