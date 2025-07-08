from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Scf",)


class Scf(SimpleKeywordBox):
    """Enum to store all simple keywords of type Scf."""

    G3CONV = SimpleKeyword("3conv")
    """SimpleKeyword: SCF solver combination."""
    AODIISTRAH = SimpleKeyword("aodiistrah")
    """SimpleKeyword: SCF solver combination."""
    DIISTRAH = SimpleKeyword("diistrah")
    """SimpleKeyword: SCF solver combination."""
    KDIISTRAH = SimpleKeyword("kdiistrah")
    """SimpleKeyword: SCF solver combination."""
    DIIS = SimpleKeyword("diis")
    """SimpleKeyword: SCF solver."""
    NODIIS = SimpleKeyword("nodiis")
    """SimpleKeyword: SCF solver."""
    AODIIS = SimpleKeyword("aodiis")
    """SimpleKeyword: SCF solver."""
    NOAODIIS = SimpleKeyword("noaodiis")
    """SimpleKeyword: SCF solver."""
    KDIIS = SimpleKeyword("kdiis")
    """SimpleKeyword: SCF solver."""
    NOKDIIS = SimpleKeyword("nokdiis")
    """SimpleKeyword: SCF solver."""
    SOSCF = SimpleKeyword("soscf")
    """SimpleKeyword: SCF solver."""
    NOSOSCF = SimpleKeyword("nososcf")
    """SimpleKeyword: SCF solver."""
    TRAH = SimpleKeyword("trah")
    """SimpleKeyword: SCF solver."""
    NOTRAH = SimpleKeyword("notrah")
    """SimpleKeyword: SCF solver."""
    AUTOSTART = SimpleKeyword("autostart")
    """SimpleKeyword: SCF initial guess start SCF from a gbw file with the same basename (default)."""
    NOAUTOSTART = SimpleKeyword("noautostart")
    """SimpleKeyword: SCF initial guess do not start SCF from a gbw file with the same basename."""
    MOREAD = SimpleKeyword("moread")
    """SimpleKeyword: SCF initial guess read orbitals from gbw file."""
    EHTANO = SimpleKeyword("ehtano")
    """SimpleKeyword: SCF initial guess."""
    HCORE = SimpleKeyword("hcore")
    """SimpleKeyword: SCF initial guess."""
    HUECKEL = SimpleKeyword("hueckel")
    """SimpleKeyword: SCF initial guess."""
    PATOM = SimpleKeyword("patom")
    """SimpleKeyword: SCF initial guess."""
    PMODEL = SimpleKeyword("pmodel")
    """SimpleKeyword: SCF initial guess."""
    PMODELX = SimpleKeyword("pmodelx")
    """SimpleKeyword: SCF initial guess."""
    PMODELXAV = SimpleKeyword("pmodelxav")
    """SimpleKeyword: SCF initial guess."""
    PMODELXPM = SimpleKeyword("pmodelxpm")
    """SimpleKeyword: SCF initial guess."""
    SYMBREAKGUESS = SimpleKeyword("symbreakguess")
    """SimpleKeyword: SCF initial guess."""
    UNITMATRIXGUESS = SimpleKeyword("unitmatrixguess")
    """SimpleKeyword: SCF initial guess."""
    USEGRAMSCHMIDT = SimpleKeyword("usegramschmidt")
    """SimpleKeyword: SCF initial guess."""
    CALCGUESSENERGY = SimpleKeyword("calcguessenergy")
    """SimpleKeyword: Calculate the guess energy."""
    CONV = SimpleKeyword("conv")
    """SimpleKeyword: Conventional SCF."""
    SEMIDIRECT = SimpleKeyword("semidirect")
    """SimpleKeyword: Semidirect SCF."""
    DIRECT = SimpleKeyword("direct")
    """SimpleKeyword: Direct SCF."""
    SCFSTAB = SimpleKeyword("scfstab")
    """SimpleKeyword: SCF stability analysis."""
    NOSCFSTAB = SimpleKeyword("noscfstab")
    """SimpleKeyword: No SCF stability analysis."""
    DELTASCF = SimpleKeyword("deltascf")
    """SimpleKeyword: DeltaSCF for access to excited states."""
    FRSOSCF = SimpleKeyword("frsoscf")
    """SimpleKeyword: freeze and release DeltaSCF settings."""
    GMF = SimpleKeyword("gmf")
    """SimpleKeyword: DeltaSCF settings."""
    SMEAR = SimpleKeyword("smear")
    """SimpleKeyword: do finite temperature DFT (smearing)."""
    NOSMEAR = SimpleKeyword("nosmear")
    """SimpleKeyword: do not use finite temperature DFT (smearing)."""
    FRACOCC = SimpleKeyword("fracocc")
    """SimpleKeyword: enable fractional occupations."""
    SCFCONVFORCED = SimpleKeyword("scfconvforced")
    """SimpleKeyword: Force SCF convergence for subsequent operations."""
    SLOPPYSCF = SimpleKeyword("sloppyscf")
    """SimpleKeyword: SCF convergence threshold settings."""
    LOOSESCF = SimpleKeyword("loosescf")
    """SimpleKeyword: SCF convergence threshold settings."""
    NORMALSCF = SimpleKeyword("normalscf")
    """SimpleKeyword: SCF convergence threshold settings."""
    STRONGSCF = SimpleKeyword("strongscf")
    """SimpleKeyword: SCF convergence threshold settings."""
    TIGHTSCF = SimpleKeyword("tightscf")
    """SimpleKeyword: SCF convergence threshold settings."""
    VERYTIGHTSCF = SimpleKeyword("verytightscf")
    """SimpleKeyword: SCF convergence threshold settings."""
    EXTREMESCF = SimpleKeyword("extremescf")
    """SimpleKeyword: SCF convergence threshold settings."""
    SLOPPYSCFCHECK = SimpleKeyword("sloppyscfcheck")
    """SimpleKeyword: SCF convergence threshold settings."""
    NOSLOPPYSCFCHECK = SimpleKeyword("nosloppyscfcheck")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCHECKGRAD = SimpleKeyword("scfcheckgrad")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV6 = SimpleKeyword("scfconv6")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV7 = SimpleKeyword("scfconv7")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV8 = SimpleKeyword("scfconv8")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV9 = SimpleKeyword("scfconv9")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV10 = SimpleKeyword("scfconv10")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV11 = SimpleKeyword("scfconv11")
    """SimpleKeyword: SCF convergence threshold settings."""
    SCFCONV12 = SimpleKeyword("scfconv12")
    """SimpleKeyword: SCF convergence threshold settings."""
    EASYCONV = SimpleKeyword("easyconv")
    """SimpleKeyword: SCF convergence strategy."""
    NORMALCONV = SimpleKeyword("normalconv")
    """SimpleKeyword: SCF convergence strategy."""
    SLOWCONV = SimpleKeyword("slowconv")
    """SimpleKeyword: SCF convergence strategy."""
    VERYSLOWCONV = SimpleKeyword("veryslowconv")
    """SimpleKeyword: SCF convergence strategy."""
    DAMP = SimpleKeyword("damp")
    """SimpleKeyword: SCF settings."""
    NODAMP = SimpleKeyword("nodamp")
    """SimpleKeyword: SCF settings."""
    LSHIFT = SimpleKeyword("lshift")
    """SimpleKeyword: SCF settings."""
    NOLSHIFT = SimpleKeyword("nolshift")
    """SimpleKeyword: SCF settings."""
    USEINCREMENTAL = SimpleKeyword("useincremental")
    """SimpleKeyword: SCF settings."""
    NOINCREMENTAL = SimpleKeyword("noincremental")
    """SimpleKeyword: SCF settings."""
    NOITER = SimpleKeyword("noiter")
    """SimpleKeyword: SCF settings no iterations."""
    SCFLBFGS = SimpleKeyword("scflbfgs")
    """SimpleKeyword: SOSCF settings."""
    SCFLBOFILL = SimpleKeyword("scflbofill")
    """SimpleKeyword: SOSCF settings."""
    SCFLPOWELL = SimpleKeyword("scflpowell")
    """SimpleKeyword: SOSCF settings."""
    SCFLSR1 = SimpleKeyword("scflsr1")
    """SimpleKeyword: SOSCF settings."""
    NOTRAHRANDOMIZE = SimpleKeyword("notrahrandomize")
    """SimpleKeyword: TRAH settings."""
