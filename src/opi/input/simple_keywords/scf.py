from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Scf",)


class ScfThreshold(SimpleKeywordBox):
    SLOPPYSCF = ORCAKeyword("sloppyscf", alias="sloppy")
    """ORCAKeyword: SCF convergence threshold settings."""
    LOOSESCF = ORCAKeyword("loosescf", alias="loose")
    """ORCAKeyword: SCF convergence threshold settings."""
    NORMALSCF = ORCAKeyword("normalscf", alias="normal")
    """ORCAKeyword: SCF convergence threshold settings."""
    STRONGSCF = ORCAKeyword("strongscf", alias="strong")
    """ORCAKeyword: SCF convergence threshold settings."""
    TIGHTSCF = ORCAKeyword("tightscf", alias="tight")
    """ORCAKeyword: SCF convergence threshold settings."""
    VERYTIGHTSCF = ORCAKeyword("verytightscf", alias="verytight")
    """ORCAKeyword: SCF convergence threshold settings."""
    EXTREMESCF = ORCAKeyword("extremescf", alias="extreme")
    """ORCAKeyword: SCF convergence threshold settings."""


class ScfGuess(SimpleKeywordBox):
    MOREAD = ORCAKeyword("moread")
    """ORCAKeyword: SCF initial guess read orbitals from gbw file."""
    EHTANO = ORCAKeyword("ehtano")
    """ORCAKeyword: SCF initial guess."""
    HCORE = ORCAKeyword("hcore")
    """ORCAKeyword: SCF initial guess."""
    PATOM = ORCAKeyword("patom")
    """ORCAKeyword: SCF initial guess."""
    PMODEL = ORCAKeyword("pmodel")
    """ORCAKeyword: SCF initial guess."""
    PMODELX = ORCAKeyword("pmodelx")
    """ORCAKeyword: SCF initial guess."""
    PMODELXAV = ORCAKeyword("pmodelxav")
    """ORCAKeyword: SCF initial guess."""
    PMODELXPM = ORCAKeyword("pmodelxpm")
    """ORCAKeyword: SCF initial guess."""
    SYMBREAKGUESS = ORCAKeyword("symbreakguess")
    """ORCAKeyword: SCF initial guess."""


class ScfConvergence(SimpleKeywordBox):
    EASYCONV = ORCAKeyword("easyconv", alias="easy")
    """ORCAKeyword: SCF convergence strategy."""
    NORMALCONV = ORCAKeyword("normalconv", alias="normal")
    """ORCAKeyword: SCF convergence strategy."""
    SLOWCONV = ORCAKeyword("slowconv", alias="slow")
    """ORCAKeyword: SCF convergence strategy."""
    VERYSLOWCONV = ORCAKeyword("veryslowconv", alias="veryslow")
    """ORCAKeyword: SCF convergence strategy."""


class ScfSolver(SimpleKeywordBox):
    DIIS = ORCAKeyword("diis")
    """ORCAKeyword: SCF solver."""
    KDIIS = ORCAKeyword("kdiis")
    """ORCAKeyword: SCF solver."""
    SOSCF = ORCAKeyword("soscf")
    """ORCAKeyword: SCF solver."""
    TRAH = ORCAKeyword("trah")
    """ORCAKeyword: SCF solver."""


class Scf(ScfThreshold, ScfConvergence, ScfGuess, ScfSolver):
    """Enum to store all simple keywords of type Scf."""

    G3CONV = ORCAKeyword("3conv")
    """ORCAKeyword: SCF solver combination."""
    AODIISTRAH = ORCAKeyword("aodiistrah")
    """ORCAKeyword: SCF solver combination."""
    DIISTRAH = ORCAKeyword("diistrah")
    """ORCAKeyword: SCF solver combination."""
    KDIISTRAH = ORCAKeyword("kdiistrah")
    """ORCAKeyword: SCF solver combination."""

    NODIIS = ORCAKeyword("nodiis")
    """ORCAKeyword: SCF solver."""
    AODIIS = ORCAKeyword("aodiis")
    """ORCAKeyword: SCF solver."""
    NOAODIIS = ORCAKeyword("noaodiis")
    """ORCAKeyword: SCF solver."""

    NOKDIIS = ORCAKeyword("nokdiis")
    """ORCAKeyword: SCF solver."""

    NOSOSCF = ORCAKeyword("nososcf")
    """ORCAKeyword: SCF solver."""

    NOTRAH = ORCAKeyword("notrah")
    """ORCAKeyword: SCF solver."""
    AUTOSTART = ORCAKeyword("autostart")
    """ORCAKeyword: SCF initial guess start SCF from a gbw file with the same basename (default)."""
    NOAUTOSTART = ORCAKeyword("noautostart")
    """ORCAKeyword: SCF initial guess do not start SCF from a gbw file with the same basename."""
    HUECKEL = ORCAKeyword("hueckel")
    """ORCAKeyword: SCF initial guess."""

    UNITMATRIXGUESS = ORCAKeyword("unitmatrixguess")
    """ORCAKeyword: SCF initial guess."""
    USEGRAMSCHMIDT = ORCAKeyword("usegramschmidt")
    """ORCAKeyword: SCF initial guess."""
    CALCGUESSENERGY = ORCAKeyword("calcguessenergy")
    """ORCAKeyword: Calculate the guess energy."""
    CONV = ORCAKeyword("conv")
    """ORCAKeyword: Conventional SCF."""
    SEMIDIRECT = ORCAKeyword("semidirect")
    """ORCAKeyword: Semidirect SCF."""
    DIRECT = ORCAKeyword("direct")
    """ORCAKeyword: Direct SCF."""
    SCFSTAB = ORCAKeyword("scfstab")
    """ORCAKeyword: SCF stability analysis."""
    NOSCFSTAB = ORCAKeyword("noscfstab")
    """ORCAKeyword: No SCF stability analysis."""
    DELTASCF = ORCAKeyword("deltascf")
    """ORCAKeyword: DeltaSCF for access to excited states."""
    FRSOSCF = ORCAKeyword("frsoscf")
    """ORCAKeyword: freeze and release DeltaSCF settings."""
    GMF = ORCAKeyword("gmf")
    """ORCAKeyword: DeltaSCF settings."""
    SMEAR = ORCAKeyword("smear")
    """ORCAKeyword: do finite temperature DFT (smearing)."""
    NOSMEAR = ORCAKeyword("nosmear")
    """ORCAKeyword: do not use finite temperature DFT (smearing)."""
    FRACOCC = ORCAKeyword("fracocc")
    """ORCAKeyword: enable fractional occupations."""
    SCFCONVFORCED = ORCAKeyword("scfconvforced")
    """ORCAKeyword: Force SCF convergence for subsequent operations."""
    SLOPPYSCFCHECK = ORCAKeyword("sloppyscfcheck")
    """ORCAKeyword: SCF convergence threshold settings."""
    NOSLOPPYSCFCHECK = ORCAKeyword("nosloppyscfcheck")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCHECKGRAD = ORCAKeyword("scfcheckgrad")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV6 = ORCAKeyword("scfconv6")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV7 = ORCAKeyword("scfconv7")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV8 = ORCAKeyword("scfconv8")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV9 = ORCAKeyword("scfconv9")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV10 = ORCAKeyword("scfconv10")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV11 = ORCAKeyword("scfconv11")
    """ORCAKeyword: SCF convergence threshold settings."""
    SCFCONV12 = ORCAKeyword("scfconv12")
    """ORCAKeyword: SCF convergence threshold settings."""
    DAMP = ORCAKeyword("damp")
    """ORCAKeyword: SCF settings."""
    NODAMP = ORCAKeyword("nodamp")
    """ORCAKeyword: SCF settings."""
    LSHIFT = ORCAKeyword("lshift")
    """ORCAKeyword: SCF settings."""
    NOLSHIFT = ORCAKeyword("nolshift")
    """ORCAKeyword: SCF settings."""
    USEINCREMENTAL = ORCAKeyword("useincremental")
    """ORCAKeyword: SCF settings."""
    NOINCREMENTAL = ORCAKeyword("noincremental")
    """ORCAKeyword: SCF settings."""
    NOITER = ORCAKeyword("noiter")
    """ORCAKeyword: SCF settings no iterations."""
    SCFLBFGS = ORCAKeyword("scflbfgs")
    """ORCAKeyword: SOSCF settings."""
    SCFLBOFILL = ORCAKeyword("scflbofill")
    """ORCAKeyword: SOSCF settings."""
    SCFLPOWELL = ORCAKeyword("scflpowell")
    """ORCAKeyword: SOSCF settings."""
    SCFLSR1 = ORCAKeyword("scflsr1")
    """ORCAKeyword: SOSCF settings."""
    NOTRAHRANDOMIZE = ORCAKeyword("notrahrandomize")
    """ORCAKeyword: TRAH settings."""
