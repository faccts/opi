from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Task",)


class Task(SimpleKeywordBox):
    """Enum to store all simple keywords of type Task.

    Attributes
    ----------
    SP : SimpleKeyword
        perform a single point energy calculation (default)
    ENGRAD : SimpleKeyword
        Energy and gradient
    OPT : SimpleKeyword
        Perform geometry optimization
    FREQ : SimpleKeyword
        analytical frequency calculation
    NUMFREQ : SimpleKeyword
        numerical frequency calculation
    MD : SimpleKeyword
        molecular dynamics
    EDA : SimpleKeyword
        Perform an eda analysis
    AUTOFRAG : SimpleKeyword
        Automatic detection of fragments
    CIM : SimpleKeyword
        Calculate energy with clusters in molecule approach
    CRUDEOPT : SimpleKeyword
        Geometry optimization with thresholds
    LOOSEOPT : SimpleKeyword
        Geometry optimization with thresholds
    NORMALOPT : SimpleKeyword
        Geometry optimization with thresholds
    SLOPPYOPT : SimpleKeyword
        Geometry optimization with thresholds
    TIGHTOPT : SimpleKeyword
        Geometry optimization with thresholds
    VERYTIGHTOPT : SimpleKeyword
        Geometry optimization with thresholds
    OPTH : SimpleKeyword
        Optimize only hydrogen atoms
    COPT : SimpleKeyword
        Perform geometry optimization (cartesian coordinates)
    L_OPT : SimpleKeyword
        Perform geometry optimization with lopt
    L_OPTH : SimpleKeyword
        Optimize only hydrogen atoms
    EXTOPT : SimpleKeyword
        Use only the geometry optimizer from orca with external energy/gradient
    OPTTS : SimpleKeyword
        optimize transition state
    OPTTS_GMF : SimpleKeyword
        optimize transition state
    QMMMOPT : SimpleKeyword
        Optimize the geometry with qmmm
    QMMMOPT_PDYNAMO : SimpleKeyword
        Optimize the geometry with qmmm
    RIGIDBODYOPT : SimpleKeyword
        Optimize fragments as rigid bodies
    CI_OPT : SimpleKeyword
        conical-intersection optimization
    MECP_OPT : SimpleKeyword
        MECP optimization
    NEB : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_CI : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_IDPP : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_MMFTS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    FAST_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    LOOSE_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    TIGHT_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB_CI : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    FLAT_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    IRC : SimpleKeyword
        internal reaction coordinate
    SCANTS : SimpleKeyword
        scan for transition state
    GOAT : SimpleKeyword
        GOAT Methods
    GOAT_COARSE : SimpleKeyword
        GOAT Methods
    GOAT_DIVERSITY : SimpleKeyword
        GOAT Methods
    GOAT_ENTROPY : SimpleKeyword
        GOAT Methods
    GOAT_EXPLORE : SimpleKeyword
        GOAT Methods
    GOAT_REACT : SimpleKeyword
        GOAT Methods
    GOAT_TS : SimpleKeyword
        GOAT Methods
    NORMALDOCK : SimpleKeyword
        Docker Methods
    COMPLETEDOCK : SimpleKeyword
        Docker Methods
    DOCK_GFN_FF : SimpleKeyword
        Docker Methods
    DOCK_GFN0_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFN1_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFN2_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFNFF : SimpleKeyword
        Docker Methods
    DOCK_XTB : SimpleKeyword
        Docker Methods
    DOCK_XTB0 : SimpleKeyword
        Docker Methods
    DOCK_XTB1 : SimpleKeyword
        Docker Methods
    DOCKER : SimpleKeyword
        Docker Methods
    DOCKER_GFN_FF : SimpleKeyword
        Docker Methods
    DOCKER_GFN0_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFN1_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFN2_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFNFF : SimpleKeyword
        Docker Methods
    DOCKER_XTB : SimpleKeyword
        Docker Methods
    DOCKER_XTB0 : SimpleKeyword
        Docker Methods
    DOCKER_XTB1 : SimpleKeyword
        Docker Methods
    QUICKDOCK : SimpleKeyword
        Docker Methods
    SCREENDOCK : SimpleKeyword
        Docker Methods
    SOLVATOR : SimpleKeyword
        Use the solvator for explicit solvation
    ENMGRAD : SimpleKeyword
        Energy normal mode gradient
    CALCESTHESS : SimpleKeyword
        Calculate an approximate hessian
    MT : SimpleKeyword
        mode trajectory
    NMSCAN : SimpleKeyword
        normal mode scan
    PRINTTHERMOCHEM : SimpleKeyword
        Only do thermostatistical corrections
    PROPERTIESONLY : SimpleKeyword
        Only calc properties
    NUMNAC : SimpleKeyword
        Numerical non-adiabatic coupling
    """

    SP = SimpleKeyword("sp")
    ENGRAD = SimpleKeyword("engrad")
    OPT = SimpleKeyword("opt")
    FREQ = SimpleKeyword("freq")
    NUMFREQ = SimpleKeyword("numfreq")
    MD = SimpleKeyword("md")
    EDA = SimpleKeyword("eda")
    AUTOFRAG = SimpleKeyword("autofrag")
    CIM = SimpleKeyword("cim")
    CRUDEOPT = SimpleKeyword("crudeopt")
    LOOSEOPT = SimpleKeyword("looseopt")
    NORMALOPT = SimpleKeyword("normalopt")
    SLOPPYOPT = SimpleKeyword("sloppyopt")
    TIGHTOPT = SimpleKeyword("tightopt")
    VERYTIGHTOPT = SimpleKeyword("verytightopt")
    OPTH = SimpleKeyword("opth")
    COPT = SimpleKeyword("copt")
    L_OPT = SimpleKeyword("l-opt")
    L_OPTH = SimpleKeyword("l-opth")
    EXTOPT = SimpleKeyword("extopt")
    OPTTS = SimpleKeyword("optts")
    OPTTS_GMF = SimpleKeyword("optts(gmf)")
    QMMMOPT = SimpleKeyword("qmmmopt")
    QMMMOPT_PDYNAMO = SimpleKeyword("qmmmopt/pdynamo")
    RIGIDBODYOPT = SimpleKeyword("rigidbodyopt")
    CI_OPT = SimpleKeyword("ci-opt")
    MECP_OPT = SimpleKeyword("mecp-opt")
    NEB = SimpleKeyword("neb")
    NEB_CI = SimpleKeyword("neb-ci")
    NEB_IDPP = SimpleKeyword("neb-idpp")
    NEB_MMFTS = SimpleKeyword("neb-mmfts")
    NEB_TS = SimpleKeyword("neb-ts")
    FAST_NEB_TS = SimpleKeyword("fast-neb-ts")
    LOOSE_NEB_TS = SimpleKeyword("loose-neb-ts")
    TIGHT_NEB_TS = SimpleKeyword("tight-neb-ts")
    ZOOM_NEB = SimpleKeyword("zoom-neb")
    ZOOM_NEB_CI = SimpleKeyword("zoom-neb-ci")
    ZOOM_NEB_TS = SimpleKeyword("zoom-neb-ts")
    FLAT_NEB_TS = SimpleKeyword("flat-neb-ts")
    IRC = SimpleKeyword("irc")
    SCANTS = SimpleKeyword("scants")
    GOAT = SimpleKeyword("goat")
    GOAT_COARSE = SimpleKeyword("goat-coarse")
    GOAT_DIVERSITY = SimpleKeyword("goat-diversity")
    GOAT_ENTROPY = SimpleKeyword("goat-entropy")
    GOAT_EXPLORE = SimpleKeyword("goat-explore")
    GOAT_REACT = SimpleKeyword("goat-react")
    GOAT_TS = SimpleKeyword("goat-ts")
    NORMALDOCK = SimpleKeyword("normaldock")
    COMPLETEDOCK = SimpleKeyword("completedock")
    DOCK_GFN_FF = SimpleKeyword("dock(gfn-ff)")
    DOCK_GFN0_XTB = SimpleKeyword("dock(gfn0-xtb)")
    DOCK_GFN1_XTB = SimpleKeyword("dock(gfn1-xtb)")
    DOCK_GFN2_XTB = SimpleKeyword("dock(gfn2-xtb)")
    DOCK_GFNFF = SimpleKeyword("dock(gfnff)")
    DOCK_XTB = SimpleKeyword("dock(xtb)")
    DOCK_XTB0 = SimpleKeyword("dock(xtb0)")
    DOCK_XTB1 = SimpleKeyword("dock(xtb1)")
    DOCKER = SimpleKeyword("docker")
    DOCKER_GFN_FF = SimpleKeyword("docker(gfn-ff)")
    DOCKER_GFN0_XTB = SimpleKeyword("docker(gfn0-xtb)")
    DOCKER_GFN1_XTB = SimpleKeyword("docker(gfn1-xtb)")
    DOCKER_GFN2_XTB = SimpleKeyword("docker(gfn2-xtb)")
    DOCKER_GFNFF = SimpleKeyword("docker(gfnff)")
    DOCKER_XTB = SimpleKeyword("docker(xtb)")
    DOCKER_XTB0 = SimpleKeyword("docker(xtb0)")
    DOCKER_XTB1 = SimpleKeyword("docker(xtb1)")
    QUICKDOCK = SimpleKeyword("quickdock")
    SCREENDOCK = SimpleKeyword("screendock")
    SOLVATOR = SimpleKeyword("solvator")
    ENMGRAD = SimpleKeyword("enmgrad")
    CALCESTHESS = SimpleKeyword("calcesthess")
    MT = SimpleKeyword("mt")
    NMSCAN = SimpleKeyword("nmscan")
    PRINTTHERMOCHEM = SimpleKeyword("printthermochem")
    PROPERTIESONLY = SimpleKeyword("propertiesonly")
    NUMNAC = SimpleKeyword("numnac")
