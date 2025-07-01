from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Scf",)


class Scf(SimpleKeywordBox):
    """Enum to store all simple keywords of type Scf.

    Attributes
    ----------
    G3CONV : SimpleKeyword
        SCF solver combination
    AODIISTRAH : SimpleKeyword
        SCF solver combination
    DIISTRAH : SimpleKeyword
        SCF solver combination
    KDIISTRAH : SimpleKeyword
        SCF solver combination
    DIIS : SimpleKeyword
        SCF solver
    NODIIS : SimpleKeyword
        SCF solver
    AODIIS : SimpleKeyword
        SCF solver
    NOAODIIS : SimpleKeyword
        SCF solver
    KDIIS : SimpleKeyword
        SCF solver
    NOKDIIS : SimpleKeyword
        SCF solver
    SOSCF : SimpleKeyword
        SCF solver
    NOSOSCF : SimpleKeyword
        SCF solver
    TRAH : SimpleKeyword
        SCF solver
    NOTRAH : SimpleKeyword
        SCF solver
    AUTOSTART : SimpleKeyword
        SCF initial guess start SCF from a gbw file with the same basename (default)
    NOAUTOSTART : SimpleKeyword
        SCF initial guess do not start SCF from a gbw file with the same basename
    MOREAD : SimpleKeyword
        SCF initial guess read orbitals from gbw file
    EHTANO : SimpleKeyword
        SCF initial guess
    HCORE : SimpleKeyword
        SCF initial guess
    HUECKEL : SimpleKeyword
        SCF initial guess
    PATOM : SimpleKeyword
        SCF initial guess
    PMODEL : SimpleKeyword
        SCF initial guess
    PMODELX : SimpleKeyword
        SCF initial guess
    PMODELXAV : SimpleKeyword
        SCF initial guess
    PMODELXPM : SimpleKeyword
        SCF initial guess
    SYMBREAKGUESS : SimpleKeyword
        SCF initial guess
    UNITMATRIXGUESS : SimpleKeyword
        SCF initial guess
    USEGRAMSCHMIDT : SimpleKeyword
        SCF initial guess
    CALCGUESSENERGY : SimpleKeyword
        Calculate the guess energy
    CONV : SimpleKeyword
        Conventional SCF
    SEMIDIRECT : SimpleKeyword
        Semidirect SCF
    DIRECT : SimpleKeyword
        Direct SCF
    SCFSTAB : SimpleKeyword
        SCF stability analysis
    NOSCFSTAB : SimpleKeyword
        No SCF stability analysis
    DELTASCF : SimpleKeyword
        DeltaSCF for access to excited states
    FRSOSCF : SimpleKeyword
        freeze and release DeltaSCF settings
    GMF : SimpleKeyword
        DeltaSCF settings
    SMEAR : SimpleKeyword
        do finite temperature DFT (smearing)
    NOSMEAR : SimpleKeyword
        do not use finite temperature DFT (smearing)
    FRACOCC : SimpleKeyword
        enable fractional occupations
    SCFCONVFORCED : SimpleKeyword
        Force SCF convergence for subsequent operations
    SLOPPYSCF : SimpleKeyword
        SCF convergence threshold settings
    LOOSESCF : SimpleKeyword
        SCF convergence threshold settings
    NORMALSCF : SimpleKeyword
        SCF convergence threshold settings
    STRONGSCF : SimpleKeyword
        SCF convergence threshold settings
    TIGHTSCF : SimpleKeyword
        SCF convergence threshold settings
    VERYTIGHTSCF : SimpleKeyword
        SCF convergence threshold settings
    EXTREMESCF : SimpleKeyword
        SCF convergence threshold settings
    SLOPPYSCFCHECK : SimpleKeyword
        SCF convergence threshold settings
    NOSLOPPYSCFCHECK : SimpleKeyword
        SCF convergence threshold settings
    SCFCHECKGRAD : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV6 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV7 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV8 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV9 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV10 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV11 : SimpleKeyword
        SCF convergence threshold settings
    SCFCONV12 : SimpleKeyword
        SCF convergence threshold settings
    EASYCONV : SimpleKeyword
        SCF convergence strategy
    NORMALCONV : SimpleKeyword
        SCF convergence strategy
    SLOWCONV : SimpleKeyword
        SCF convergence strategy
    VERYSLOWCONV : SimpleKeyword
        SCF convergence strategy
    DAMP : SimpleKeyword
        SCF settings
    NODAMP : SimpleKeyword
        SCF settings
    LSHIFT : SimpleKeyword
        SCF settings
    NOLSHIFT : SimpleKeyword
        SCF settings
    USEINCREMENTAL : SimpleKeyword
        SCF settings
    NOINCREMENTAL : SimpleKeyword
        SCF settings
    NOITER : SimpleKeyword
        SCF settings no iterations
    SCFLBFGS : SimpleKeyword
        SOSCF settings
    SCFLBOFILL : SimpleKeyword
        SOSCF settings
    SCFLPOWELL : SimpleKeyword
        SOSCF settings
    SCFLSR1 : SimpleKeyword
        SOSCF settings
    NOTRAHRANDOMIZE : SimpleKeyword
        TRAH settings
    """

    G3CONV = SimpleKeyword("3conv")
    AODIISTRAH = SimpleKeyword("aodiistrah")
    DIISTRAH = SimpleKeyword("diistrah")
    KDIISTRAH = SimpleKeyword("kdiistrah")
    DIIS = SimpleKeyword("diis")
    NODIIS = SimpleKeyword("nodiis")
    AODIIS = SimpleKeyword("aodiis")
    NOAODIIS = SimpleKeyword("noaodiis")
    KDIIS = SimpleKeyword("kdiis")
    NOKDIIS = SimpleKeyword("nokdiis")
    SOSCF = SimpleKeyword("soscf")
    NOSOSCF = SimpleKeyword("nososcf")
    TRAH = SimpleKeyword("trah")
    NOTRAH = SimpleKeyword("notrah")
    AUTOSTART = SimpleKeyword("autostart")
    NOAUTOSTART = SimpleKeyword("noautostart")
    MOREAD = SimpleKeyword("moread")
    EHTANO = SimpleKeyword("ehtano")
    HCORE = SimpleKeyword("hcore")
    HUECKEL = SimpleKeyword("hueckel")
    PATOM = SimpleKeyword("patom")
    PMODEL = SimpleKeyword("pmodel")
    PMODELX = SimpleKeyword("pmodelx")
    PMODELXAV = SimpleKeyword("pmodelxav")
    PMODELXPM = SimpleKeyword("pmodelxpm")
    SYMBREAKGUESS = SimpleKeyword("symbreakguess")
    UNITMATRIXGUESS = SimpleKeyword("unitmatrixguess")
    USEGRAMSCHMIDT = SimpleKeyword("usegramschmidt")
    CALCGUESSENERGY = SimpleKeyword("calcguessenergy")
    CONV = SimpleKeyword("conv")
    SEMIDIRECT = SimpleKeyword("semidirect")
    DIRECT = SimpleKeyword("direct")
    SCFSTAB = SimpleKeyword("scfstab")
    NOSCFSTAB = SimpleKeyword("noscfstab")
    DELTASCF = SimpleKeyword("deltascf")
    FRSOSCF = SimpleKeyword("frsoscf")
    GMF = SimpleKeyword("gmf")
    SMEAR = SimpleKeyword("smear")
    NOSMEAR = SimpleKeyword("nosmear")
    FRACOCC = SimpleKeyword("fracocc")
    SCFCONVFORCED = SimpleKeyword("scfconvforced")
    SLOPPYSCF = SimpleKeyword("sloppyscf")
    LOOSESCF = SimpleKeyword("loosescf")
    NORMALSCF = SimpleKeyword("normalscf")
    STRONGSCF = SimpleKeyword("strongscf")
    TIGHTSCF = SimpleKeyword("tightscf")
    VERYTIGHTSCF = SimpleKeyword("verytightscf")
    EXTREMESCF = SimpleKeyword("extremescf")
    SLOPPYSCFCHECK = SimpleKeyword("sloppyscfcheck")
    NOSLOPPYSCFCHECK = SimpleKeyword("nosloppyscfcheck")
    SCFCHECKGRAD = SimpleKeyword("scfcheckgrad")
    SCFCONV6 = SimpleKeyword("scfconv6")
    SCFCONV7 = SimpleKeyword("scfconv7")
    SCFCONV8 = SimpleKeyword("scfconv8")
    SCFCONV9 = SimpleKeyword("scfconv9")
    SCFCONV10 = SimpleKeyword("scfconv10")
    SCFCONV11 = SimpleKeyword("scfconv11")
    SCFCONV12 = SimpleKeyword("scfconv12")
    EASYCONV = SimpleKeyword("easyconv")
    NORMALCONV = SimpleKeyword("normalconv")
    SLOWCONV = SimpleKeyword("slowconv")
    VERYSLOWCONV = SimpleKeyword("veryslowconv")
    DAMP = SimpleKeyword("damp")
    NODAMP = SimpleKeyword("nodamp")
    LSHIFT = SimpleKeyword("lshift")
    NOLSHIFT = SimpleKeyword("nolshift")
    USEINCREMENTAL = SimpleKeyword("useincremental")
    NOINCREMENTAL = SimpleKeyword("noincremental")
    NOITER = SimpleKeyword("noiter")
    SCFLBFGS = SimpleKeyword("scflbfgs")
    SCFLBOFILL = SimpleKeyword("scflbofill")
    SCFLPOWELL = SimpleKeyword("scflpowell")
    SCFLSR1 = SimpleKeyword("scflsr1")
    NOTRAHRANDOMIZE = SimpleKeyword("notrahrandomize")
