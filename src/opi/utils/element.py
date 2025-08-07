from opi.models.string_enum import StringEnum


class Element(StringEnum):
    """
    Class that stores a list of all elements.
    When an element is required as an input, it is to be selected from this class to avoid user error
    """

    # /// HYDROGEN
    HYDROGEN = "H"
    H = "H"
    # /// HELIUM
    HELIUM = "He"
    HE = "He"
    # /// LITHIUM
    LITHIUM = "Li"
    LI = "Li"
    # /// BERYLLIUM
    BERYLLIUM = "Be"
    BE = "Be"
    # /// BORON
    BORON = "B"
    B = "B"
    # /// CARBON
    CARBON = "C"
    C = "C"
    # /// NITROGEN
    NITROGEN = "N"
    N = "N"
    # /// OXYGEN
    OXYGEN = "O"
    O = "O"  # noqa: E741
    # /// FLUORINE
    FLUORINE = "F"
    F = "F"
    # /// NEON
    NEON = "Ne"
    NE = "Ne"
    # /// SODIUM
    SODIUM = "Na"
    NA = "Na"
    # /// MAGNESIUM
    MAGNESIUM = "Mg"
    MG = "Mg"
    # /// ALUMINUM
    ALUMINUM = "Al"
    AL = "Al"
    # /// SILICON
    SILICON = "Si"
    SI = "Si"
    # /// PHOSPHORUS
    PHOSPHORUS = "P"
    P = "P"
    # /// SULFUR
    SULFUR = "S"
    S = "S"
    # /// CHLORINE
    CHLORINE = "Cl"
    CL = "Cl"
    # /// ARGON
    ARGON = "Ar"
    AR = "Ar"
    # /// POTASSIUM
    POTASSIUM = "K"
    K = "K"
    # /// CALCIUM
    CALCIUM = "Ca"
    CA = "Ca"
    # /// SCANDIUM
    SCANDIUM = "Sc"
    SC = "Sc"
    # /// TITANIUM
    TITANIUM = "Ti"
    TI = "Ti"
    # /// VANADIUM
    VANADIUM = "V"
    V = "V"
    # /// CHROMIUM
    CHROMIUM = "Cr"
    CR = "Cr"
    # /// MANGANESE
    MANGANESE = "Mn"
    MN = "Mn"
    # /// IRON
    IRON = "Fe"
    FE = "Fe"
    # /// COBALT
    COBALT = "Co"
    CO = "Co"
    # /// NICKEL
    NICKEL = "Ni"
    NI = "Ni"
    # /// COPPER
    COPPER = "Cu"
    CU = "Cu"
    # /// ZINC
    ZINC = "Zn"
    ZN = "Zn"
    # /// GALLIUM
    GALLIUM = "Ga"
    GA = "Ga"
    # /// GERMANIUM
    GERMANIUM = "Ge"
    GE = "Ge"
    # /// ARSENIC
    ARSENIC = "As"
    AS = "As"
    # /// SELENIUM
    SELENIUM = "Se"
    SE = "Se"
    # /// BROMINE
    BROMINE = "Br"
    BR = "Br"
    # /// KRYPTON
    KRYPTON = "Kr"
    KR = "Kr"
    # /// RUBIDIUM
    RUBIDIUM = "Rb"
    RB = "Rb"
    # /// STRONTIUM
    STRONTIUM = "Sr"
    SR = "Sr"
    # /// YTTRIUM
    YTTRIUM = "Y"
    Y = "Y"
    # /// ZIRCONIUM
    ZIRCONIUM = "Zr"
    ZR = "Zr"
    # /// NIOBIUM
    NIOBIUM = "Nb"
    NB = "Nb"
    # /// MOLYBDENUM
    MOLYBDENUM = "Mo"
    MO = "Mo"
    # /// TECHNETIUM
    TECHNETIUM = "Tc"
    TC = "Tc"
    # /// RUTHENIUM
    RUTHENIUM = "Ru"
    RU = "Ru"
    # /// RHODIUM
    RHODIUM = "Rh"
    RH = "Rh"
    # /// PALLADIUM
    PALLADIUM = "Pd"
    PD = "Pd"
    # /// SILVER
    SILVER = "Ag"
    AG = "Ag"
    # /// CADMIUM
    CADMIUM = "Cd"
    CD = "Cd"
    # /// INDIUM
    INDIUM = "In"
    IN = "In"
    # /// TIN
    TIN = "Sn"
    SN = "Sn"
    # /// ANTIMONY
    ANTIMONY = "Sb"
    SB = "Sb"
    # /// TELLURIUM
    TELLURIUM = "Te"
    TE = "Te"
    # /// IODINE
    IODINE = "I"
    I = "I"  # noqa: E741
    # /// XENON
    XENON = "Xe"
    XE = "Xe"
    # /// CESIUM
    CESIUM = "Cs"
    CS = "Cs"
    # /// BARIUM
    BARIUM = "Ba"
    BA = "Ba"
    # /// LANTHANUM
    LANTHANUM = "La"
    LA = "La"
    # /// CERIUM
    CERIUM = "Ce"
    CE = "Ce"
    # /// PRASEODYMIUM
    PRASEODYMIUM = "Pr"
    PR = "Pr"
    # /// NEODYMIUM
    NEODYMIUM = "Nd"
    ND = "Nd"
    # /// PROMETHIUM
    PROMETHIUM = "Pm"
    PM = "Pm"
    # /// SAMARIUM
    SAMARIUM = "Sm"
    SM = "Sm"
    # /// EUROPIUM
    EUROPIUM = "Eu"
    EU = "Eu"
    # /// GADOLINIUM
    GADOLINIUM = "Gd"
    GD = "Gd"
    # /// TERBIUM
    TERBIUM = "Tb"
    TB = "Tb"
    # /// DYSPROSIUM
    DYSPROSIUM = "Dy"
    DY = "Dy"
    # /// HOLMIUM
    HOLMIUM = "Ho"
    HO = "Ho"
    # /// ERBIUM
    ERBIUM = "Er"
    ER = "Er"
    # /// THULIUM
    THULIUM = "Tm"
    TM = "Tm"
    # /// YTTERBIUM
    YTTERBIUM = "Yb"
    YB = "Yb"
    # /// LUTETIUM
    LUTETIUM = "Lu"
    LU = "Lu"
    # /// HAFNIUM
    HAFNIUM = "Hf"
    HF = "Hf"
    # /// TANTALUM
    TANTALUM = "Ta"
    TA = "Ta"
    # /// WOLFRAM
    WOLFRAM = "W"
    W = "W"
    # /// RHENIUM
    RHENIUM = "Re"
    RE = "Re"
    # /// OSMIUM
    OSMIUM = "Os"
    OS = "Os"
    # /// IRIDIUM
    IRIDIUM = "Ir"
    IR = "Ir"
    # /// PLATINUM
    PLATINUM = "Pt"
    PT = "Pt"
    # /// GOLD
    GOLD = "Au"
    AU = "Au"
    # /// MERCURY
    MERCURY = "Hg"
    HG = "Hg"
    # /// THALLIUM
    THALLIUM = "Tl"
    TL = "Tl"
    # /// LEAD
    LEAD = "Pb"
    PB = "Pb"
    # /// BISMUTH
    BISMUTH = "Bi"
    BI = "Bi"
    # /// POLONIUM
    POLONIUM = "Po"
    PO = "Po"
    # /// ASTATINE
    ASTATINE = "At"
    AT = "At"
    # /// RADON
    RADON = "Rn"
    RN = "Rn"
    # /// FRANCIUM
    FRANCIUM = "Fr"
    FR = "Fr"
    # /// RADIUM
    RADIUM = "Ra"
    RA = "Ra"
    # /// ACTINIUM
    ACTINIUM = "Ac"
    AC = "Ac"
    # /// THORIUM
    THORIUM = "Th"
    TH = "Th"
    # /// PROTACTINIUM
    PROTACTINIUM = "Pa"
    PA = "Pa"
    # /// URANIUM
    URANIUM = "U"
    U = "U"
    # /// NEPTUNIUM
    NEPTUNIUM = "Np"
    NP = "Np"
    # /// PLUTONIUM
    PLUTONIUM = "Pu"
    PU = "Pu"
    # /// AMERICIUM
    AMERICIUM = "Am"
    AM = "Am"
    # /// CURIUM
    CURIUM = "Cm"
    CM = "Cm"
    # /// BERKELIUM
    BERKELIUM = "Bk"
    BK = "Bk"
    # /// CALIFORNIUM
    CALIFORNIUM = "Cf"
    CF = "Cf"
    # /// EINSTEINIUM
    EINSTEINIUM = "Es"
    ES = "Es"
    # /// FERMIUM
    FERMIUM = "Fm"
    FM = "Fm"
    # /// MENDELEVIUM
    MENDELEVIUM = "Md"
    MD = "Md"
    # /// NOBELIUM
    NOBELIUM = "No"
    NO = "No"
    # /// LAWRENCIUM
    LAWRENCIUM = "Lr"
    LR = "Lr"
    # /// RUTHERFORDIUM
    RUTHERFORDIUM = "Rf"
    RF = "Rf"
    # /// DUBNIUM
    DUBNIUM = "Db"
    DB = "Db"
    # /// SEABORGIUM
    SEABORGIUM = "Sg"
    SG = "Sg"
    # /// BOHRIUM
    BOHRIUM = "Bh"
    BH = "Bh"
    # /// HASSIUM
    HASSIUM = "Hs"
    HS = "Hs"
    # /// MEITNERIUM
    MEITNERIUM = "Mt"
    MT = "Mt"
    # /// DARMSTADTIUM
    DARMSTADTIUM = "Ds"
    DS = "Ds"
    # /// ROENTGENIUM
    ROENTGENIUM = "Rg"
    RG = "Rg"
    # /// COPERNICIUM
    COPERNICIUM = "Cn"
    CN = "Cn"
    # /// NIHONIUM
    NIHONIUM = "Nh"
    NH = "Nh"
    # /// FLEROVIUM
    FLEROVIUM = "Fl"
    FL = "Fl"
    # /// MOSCOVIUM
    MOSCOVIUM = "Mc"
    MC = "Mc"
    # /// LIVERMORIUM
    LIVERMORIUM = "Lv"
    LV = "Lv"
    # /// TENNESSINE
    TENNESSINE = "Ts"
    TS = "Ts"
    # /// OGANESSON
    OGANESSON = "Og"
    OG = "Og"

    @classmethod
    def from_atomic_number(cls, atomic_number: int) -> "Element":
        """
        Get element from its atomic number.

        atomic_number: int, allowed range: 1 <= atomic_number <= 118
            Atomic number of the element

        Returns
        -------
        Element
            Returns the corresponding element

        Raises
        ------
        ValueError: Is raised if atomic number is out of range.
        """
        match atomic_number:
            case 1:
                return cls.HYDROGEN
            case 2:
                return cls.HELIUM
            case 3:
                return cls.LITHIUM
            case 4:
                return cls.BERYLLIUM
            case 5:
                return cls.BORON
            case 6:
                return cls.CARBON
            case 7:
                return cls.NITROGEN
            case 8:
                return cls.OXYGEN
            case 9:
                return cls.FLUORINE
            case 10:
                return cls.NEON
            case 11:
                return cls.SODIUM
            case 12:
                return cls.MAGNESIUM
            case 13:
                return cls.ALUMINUM
            case 14:
                return cls.SILICON
            case 15:
                return cls.PHOSPHORUS
            case 16:
                return cls.SULFUR
            case 17:
                return cls.CHLORINE
            case 18:
                return cls.ARGON
            case 19:
                return cls.POTASSIUM
            case 20:
                return cls.CALCIUM
            case 21:
                return cls.SCANDIUM
            case 22:
                return cls.TITANIUM
            case 23:
                return cls.VANADIUM
            case 24:
                return cls.CHROMIUM
            case 25:
                return cls.MANGANESE
            case 26:
                return cls.IRON
            case 27:
                return cls.COBALT
            case 28:
                return cls.NICKEL
            case 29:
                return cls.COPPER
            case 30:
                return cls.ZINC
            case 31:
                return cls.GALLIUM
            case 32:
                return cls.GERMANIUM
            case 33:
                return cls.ARSENIC
            case 34:
                return cls.SELENIUM
            case 35:
                return cls.BROMINE
            case 36:
                return cls.KRYPTON
            case 37:
                return cls.RUBIDIUM
            case 38:
                return cls.STRONTIUM
            case 39:
                return cls.YTTRIUM
            case 40:
                return cls.ZIRCONIUM
            case 41:
                return cls.NIOBIUM
            case 42:
                return cls.MOLYBDENUM
            case 43:
                return cls.TECHNETIUM
            case 44:
                return cls.RUTHENIUM
            case 45:
                return cls.RHODIUM
            case 46:
                return cls.PALLADIUM
            case 47:
                return cls.SILVER
            case 48:
                return cls.CADMIUM
            case 49:
                return cls.INDIUM
            case 50:
                return cls.TIN
            case 51:
                return cls.ANTIMONY
            case 52:
                return cls.TELLURIUM
            case 53:
                return cls.IODINE
            case 54:
                return cls.XENON
            case 55:
                return cls.CESIUM
            case 56:
                return cls.BARIUM
            case 57:
                return cls.LANTHANUM
            case 58:
                return cls.CERIUM
            case 59:
                return cls.PRASEODYMIUM
            case 60:
                return cls.NEODYMIUM
            case 61:
                return cls.PROMETHIUM
            case 62:
                return cls.SAMARIUM
            case 63:
                return cls.EUROPIUM
            case 64:
                return cls.GADOLINIUM
            case 65:
                return cls.TERBIUM
            case 66:
                return cls.DYSPROSIUM
            case 67:
                return cls.HOLMIUM
            case 68:
                return cls.ERBIUM
            case 69:
                return cls.THULIUM
            case 70:
                return cls.YTTERBIUM
            case 71:
                return cls.LUTETIUM
            case 72:
                return cls.HAFNIUM
            case 73:
                return cls.TANTALUM
            case 74:
                return cls.WOLFRAM
            case 75:
                return cls.RHENIUM
            case 76:
                return cls.OSMIUM
            case 77:
                return cls.IRIDIUM
            case 78:
                return cls.PLATINUM
            case 79:
                return cls.GOLD
            case 80:
                return cls.MERCURY
            case 81:
                return cls.THALLIUM
            case 82:
                return cls.LEAD
            case 83:
                return cls.BISMUTH
            case 84:
                return cls.POLONIUM
            case 85:
                return cls.ASTATINE
            case 86:
                return cls.RADON
            case 87:
                return cls.FRANCIUM
            case 88:
                return cls.RADIUM
            case 89:
                return cls.ACTINIUM
            case 90:
                return cls.THORIUM
            case 91:
                return cls.PROTACTINIUM
            case 92:
                return cls.URANIUM
            case 93:
                return cls.NEPTUNIUM
            case 94:
                return cls.PLUTONIUM
            case 95:
                return cls.AMERICIUM
            case 96:
                return cls.CURIUM
            case 97:
                return cls.BERKELIUM
            case 98:
                return cls.CALIFORNIUM
            case 99:
                return cls.EINSTEINIUM
            case 100:
                return cls.FERMIUM
            case 101:
                return cls.MENDELEVIUM
            case 102:
                return cls.NOBELIUM
            case 103:
                return cls.LAWRENCIUM
            case 104:
                return cls.RUTHERFORDIUM
            case 105:
                return cls.DUBNIUM
            case 106:
                return cls.SEABORGIUM
            case 107:
                return cls.BOHRIUM
            case 108:
                return cls.HASSIUM
            case 109:
                return cls.MEITNERIUM
            case 110:
                return cls.DARMSTADTIUM
            case 111:
                return cls.ROENTGENIUM
            case 112:
                return cls.COPERNICIUM
            case 113:
                return cls.NIHONIUM
            case 114:
                return cls.FLEROVIUM
            case 115:
                return cls.MOSCOVIUM
            case 116:
                return cls.LIVERMORIUM
            case 117:
                return cls.TENNESSINE
            case 118:
                return cls.OGANESSON
            case _:
                raise ValueError(f"Atomic number {atomic_number} out of range: 1 <= x <= 118")

    @classmethod
    def to_atomic_number(cls, elem: "str | Element") -> int:
        """
        Get atomic number from element label.

        Parameters
        -------
        elem: Element
            Element for which the atomic number should be returned.

        Returns
        -------
        atomic_number: int
            Returns the corresponding atomic number.

        Raises
        ------
        ValueError: Is raised if element is unknown.
        """
        if isinstance(elem, str):
            try:
                elem = cls(elem)
            except ValueError:
                raise ValueError(f"Element {elem} not known")

        match elem:
            case cls.HYDROGEN:
                return 1
            case cls.HELIUM:
                return 2
            case cls.LITHIUM:
                return 3
            case cls.BERYLLIUM:
                return 4
            case cls.BORON:
                return 5
            case cls.CARBON:
                return 6
            case cls.NITROGEN:
                return 7
            case cls.OXYGEN:
                return 8
            case cls.FLUORINE:
                return 9
            case cls.NEON:
                return 10
            case cls.SODIUM:
                return 11
            case cls.MAGNESIUM:
                return 12
            case cls.ALUMINUM:
                return 13
            case cls.SILICON:
                return 14
            case cls.PHOSPHORUS:
                return 15
            case cls.SULFUR:
                return 16
            case cls.CHLORINE:
                return 17
            case cls.ARGON:
                return 18
            case cls.POTASSIUM:
                return 19
            case cls.CALCIUM:
                return 20
            case cls.SCANDIUM:
                return 21
            case cls.TITANIUM:
                return 22
            case cls.VANADIUM:
                return 23
            case cls.CHROMIUM:
                return 24
            case cls.MANGANESE:
                return 25
            case cls.IRON:
                return 26
            case cls.COBALT:
                return 27
            case cls.NICKEL:
                return 28
            case cls.COPPER:
                return 29
            case cls.ZINC:
                return 30
            case cls.GALLIUM:
                return 31
            case cls.GERMANIUM:
                return 32
            case cls.ARSENIC:
                return 33
            case cls.SELENIUM:
                return 34
            case cls.BROMINE:
                return 35
            case cls.KRYPTON:
                return 36
            case cls.RUBIDIUM:
                return 37
            case cls.STRONTIUM:
                return 38
            case cls.YTTRIUM:
                return 39
            case cls.ZIRCONIUM:
                return 40
            case cls.NIOBIUM:
                return 41
            case cls.MOLYBDENUM:
                return 42
            case cls.TECHNETIUM:
                return 43
            case cls.RUTHENIUM:
                return 44
            case cls.RHODIUM:
                return 45
            case cls.PALLADIUM:
                return 46
            case cls.SILVER:
                return 47
            case cls.CADMIUM:
                return 48
            case cls.INDIUM:
                return 49
            case cls.TIN:
                return 50
            case cls.ANTIMONY:
                return 51
            case cls.TELLURIUM:
                return 52
            case cls.IODINE:
                return 53
            case cls.XENON:
                return 54
            case cls.CESIUM:
                return 55
            case cls.BARIUM:
                return 56
            case cls.LANTHANUM:
                return 57
            case cls.CERIUM:
                return 58
            case cls.PRASEODYMIUM:
                return 59
            case cls.NEODYMIUM:
                return 60
            case cls.PROMETHIUM:
                return 61
            case cls.SAMARIUM:
                return 62
            case cls.EUROPIUM:
                return 63
            case cls.GADOLINIUM:
                return 64
            case cls.TERBIUM:
                return 65
            case cls.DYSPROSIUM:
                return 66
            case cls.HOLMIUM:
                return 67
            case cls.ERBIUM:
                return 68
            case cls.THULIUM:
                return 69
            case cls.YTTERBIUM:
                return 70
            case cls.LUTETIUM:
                return 71
            case cls.HAFNIUM:
                return 72
            case cls.TANTALUM:
                return 73
            case cls.WOLFRAM:
                return 74
            case cls.RHENIUM:
                return 75
            case cls.OSMIUM:
                return 76
            case cls.IRIDIUM:
                return 77
            case cls.PLATINUM:
                return 78
            case cls.GOLD:
                return 79
            case cls.MERCURY:
                return 80
            case cls.THALLIUM:
                return 81
            case cls.LEAD:
                return 82
            case cls.BISMUTH:
                return 83
            case cls.POLONIUM:
                return 84
            case cls.ASTATINE:
                return 85
            case cls.RADON:
                return 86
            case cls.FRANCIUM:
                return 87
            case cls.RADIUM:
                return 88
            case cls.ACTINIUM:
                return 89
            case cls.THORIUM:
                return 90
            case cls.PROTACTINIUM:
                return 91
            case cls.URANIUM:
                return 92
            case cls.NEPTUNIUM:
                return 93
            case cls.PLUTONIUM:
                return 94
            case cls.AMERICIUM:
                return 95
            case cls.CURIUM:
                return 96
            case cls.BERKELIUM:
                return 97
            case cls.CALIFORNIUM:
                return 98
            case cls.EINSTEINIUM:
                return 99
            case cls.FERMIUM:
                return 100
            case cls.MENDELEVIUM:
                return 101
            case cls.NOBELIUM:
                return 102
            case cls.LAWRENCIUM:
                return 103
            case cls.RUTHERFORDIUM:
                return 104
            case cls.DUBNIUM:
                return 105
            case cls.SEABORGIUM:
                return 106
            case cls.BOHRIUM:
                return 107
            case cls.HASSIUM:
                return 108
            case cls.MEITNERIUM:
                return 109
            case cls.DARMSTADTIUM:
                return 110
            case cls.ROENTGENIUM:
                return 111
            case cls.COPERNICIUM:
                return 112
            case cls.NIHONIUM:
                return 113
            case cls.FLEROVIUM:
                return 114
            case cls.MOSCOVIUM:
                return 115
            case cls.LIVERMORIUM:
                return 116
            case cls.TENNESSINE:
                return 117
            case cls.OGANESSON:
                return 118
            case _:
                raise ValueError(f"Element {elem} not known")
