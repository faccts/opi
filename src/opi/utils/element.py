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

    @property
    def atomic_number(self) -> int:
        return ATOMIC_NUMBERS_FROM_ELEMENT[self]


ATOMIC_NUMBERS_FROM_ELEMENT: dict[Element, int] = {
    # 1–10
    Element.H: 1,
    Element.HYDROGEN: 1,
    Element.HE: 2,
    Element.HELIUM: 2,
    Element.LI: 3,
    Element.LITHIUM: 3,
    Element.BE: 4,
    Element.BERYLLIUM: 4,
    Element.B: 5,
    Element.BORON: 5,
    Element.C: 6,
    Element.CARBON: 6,
    Element.N: 7,
    Element.NITROGEN: 7,
    Element.O: 8,
    Element.OXYGEN: 8,
    Element.F: 9,
    Element.FLUORINE: 9,
    Element.NE: 10,
    Element.NEON: 10,
    # 11–20
    Element.NA: 11,
    Element.SODIUM: 11,
    Element.MG: 12,
    Element.MAGNESIUM: 12,
    Element.AL: 13,
    Element.ALUMINUM: 13,
    Element.SI: 14,
    Element.SILICON: 14,
    Element.P: 15,
    Element.PHOSPHORUS: 15,
    Element.S: 16,
    Element.SULFUR: 16,
    Element.CL: 17,
    Element.CHLORINE: 17,
    Element.AR: 18,
    Element.ARGON: 18,
    Element.K: 19,
    Element.POTASSIUM: 19,
    Element.CA: 20,
    Element.CALCIUM: 20,
    # 21–30
    Element.SC: 21,
    Element.SCANDIUM: 21,
    Element.TI: 22,
    Element.TITANIUM: 22,
    Element.V: 23,
    Element.VANADIUM: 23,
    Element.CR: 24,
    Element.CHROMIUM: 24,
    Element.MN: 25,
    Element.MANGANESE: 25,
    Element.FE: 26,
    Element.IRON: 26,
    Element.CO: 27,
    Element.COBALT: 27,
    Element.NI: 28,
    Element.NICKEL: 28,
    Element.CU: 29,
    Element.COPPER: 29,
    Element.ZN: 30,
    Element.ZINC: 30,
    # 31–40
    Element.GA: 31,
    Element.GALLIUM: 31,
    Element.GE: 32,
    Element.GERMANIUM: 32,
    Element.AS: 33,
    Element.ARSENIC: 33,
    Element.SE: 34,
    Element.SELENIUM: 34,
    Element.BR: 35,
    Element.BROMINE: 35,
    Element.KR: 36,
    Element.KRYPTON: 36,
    Element.RB: 37,
    Element.RUBIDIUM: 37,
    Element.SR: 38,
    Element.STRONTIUM: 38,
    Element.Y: 39,
    Element.YTTRIUM: 39,
    Element.ZR: 40,
    Element.ZIRCONIUM: 40,
    # 41–50
    Element.NB: 41,
    Element.NIOBIUM: 41,
    Element.MO: 42,
    Element.MOLYBDENUM: 42,
    Element.TC: 43,
    Element.TECHNETIUM: 43,
    Element.RU: 44,
    Element.RUTHENIUM: 44,
    Element.RH: 45,
    Element.RHODIUM: 45,
    Element.PD: 46,
    Element.PALLADIUM: 46,
    Element.AG: 47,
    Element.SILVER: 47,
    Element.CD: 48,
    Element.CADMIUM: 48,
    Element.IN: 49,
    Element.INDIUM: 49,
    Element.SN: 50,
    Element.TIN: 50,
    # 51–60
    Element.SB: 51,
    Element.ANTIMONY: 51,
    Element.TE: 52,
    Element.TELLURIUM: 52,
    Element.I: 53,
    Element.IODINE: 53,
    Element.XE: 54,
    Element.XENON: 54,
    Element.CS: 55,
    Element.CESIUM: 55,
    Element.BA: 56,
    Element.BARIUM: 56,
    Element.LA: 57,
    Element.LANTHANUM: 57,
    Element.CE: 58,
    Element.CERIUM: 58,
    Element.PR: 59,
    Element.PRASEODYMIUM: 59,
    Element.ND: 60,
    Element.NEODYMIUM: 60,
    # 61–70
    Element.PM: 61,
    Element.PROMETHIUM: 61,
    Element.SM: 62,
    Element.SAMARIUM: 62,
    Element.EU: 63,
    Element.EUROPIUM: 63,
    Element.GD: 64,
    Element.GADOLINIUM: 64,
    Element.TB: 65,
    Element.TERBIUM: 65,
    Element.DY: 66,
    Element.DYSPROSIUM: 66,
    Element.HO: 67,
    Element.HOLMIUM: 67,
    Element.ER: 68,
    Element.ERBIUM: 68,
    Element.TM: 69,
    Element.THULIUM: 69,
    Element.YB: 70,
    Element.YTTERBIUM: 70,
    # 71–80
    Element.LU: 71,
    Element.LUTETIUM: 71,
    Element.HF: 72,
    Element.HAFNIUM: 72,
    Element.TA: 73,
    Element.TANTALUM: 73,
    Element.W: 74,
    Element.WOLFRAM: 74,
    Element.RE: 75,
    Element.RHENIUM: 75,
    Element.OS: 76,
    Element.OSMIUM: 76,
    Element.IR: 77,
    Element.IRIDIUM: 77,
    Element.PT: 78,
    Element.PLATINUM: 78,
    Element.AU: 79,
    Element.GOLD: 79,
    Element.HG: 80,
    Element.MERCURY: 80,
    # 81–90
    Element.TL: 81,
    Element.THALLIUM: 81,
    Element.PB: 82,
    Element.LEAD: 82,
    Element.BI: 83,
    Element.BISMUTH: 83,
    Element.PO: 84,
    Element.POLONIUM: 84,
    Element.AT: 85,
    Element.ASTATINE: 85,
    Element.RN: 86,
    Element.RADON: 86,
    Element.FR: 87,
    Element.FRANCIUM: 87,
    Element.RA: 88,
    Element.RADIUM: 88,
    Element.AC: 89,
    Element.ACTINIUM: 89,
    Element.TH: 90,
    Element.THORIUM: 90,
    # 91–100
    Element.PA: 91,
    Element.PROTACTINIUM: 91,
    Element.U: 92,
    Element.URANIUM: 92,
    Element.NP: 93,
    Element.NEPTUNIUM: 93,
    Element.PU: 94,
    Element.PLUTONIUM: 94,
    Element.AM: 95,
    Element.AMERICIUM: 95,
    Element.CM: 96,
    Element.CURIUM: 96,
    Element.BK: 97,
    Element.BERKELIUM: 97,
    Element.CF: 98,
    Element.CALIFORNIUM: 98,
    Element.ES: 99,
    Element.EINSTEINIUM: 99,
    Element.FM: 100,
    Element.FERMIUM: 100,
    # 101–110
    Element.MD: 101,
    Element.MENDELEVIUM: 101,
    Element.NO: 102,
    Element.NOBELIUM: 102,
    Element.LR: 103,
    Element.LAWRENCIUM: 103,
    Element.RF: 104,
    Element.RUTHERFORDIUM: 104,
    Element.DB: 105,
    Element.DUBNIUM: 105,
    Element.SG: 106,
    Element.SEABORGIUM: 106,
    Element.BH: 107,
    Element.BOHRIUM: 107,
    Element.HS: 108,
    Element.HASSIUM: 108,
    Element.MT: 109,
    Element.MEITNERIUM: 109,
    Element.DS: 110,
    Element.DARMSTADTIUM: 110,
    # 111–118
    Element.RG: 111,
    Element.ROENTGENIUM: 111,
    Element.CN: 112,
    Element.COPERNICIUM: 112,
    Element.NH: 113,
    Element.NIHONIUM: 113,
    Element.FL: 114,
    Element.FLEROVIUM: 114,
    Element.MC: 115,
    Element.MOSCOVIUM: 115,
    Element.LV: 116,
    Element.LIVERMORIUM: 116,
    Element.TS: 117,
    Element.TENNESSINE: 117,
    Element.OG: 118,
    Element.OGANESSON: 118,
}
