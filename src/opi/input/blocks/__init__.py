"""
Modules that hold Python objects representing the most common block options.
"""

from opi.input.blocks.base import Block, InputFilePath, InputString, IntGroup, NumList
from opi.input.blocks.block_autoci import BlockAutoCI
from opi.input.blocks.block_basis import (
    BlockBasis,
    FragAux,
    FragAuxC,
    FragAuxJ,
    FragAuxJK,
    FragBasis,
    FragCabs,
    FragEcp,
    NewBasis,
)
from opi.input.blocks.block_casscf import BlockCasscf
from opi.input.blocks.block_cis import BlockCis
from opi.input.blocks.block_cosmors import BlockCosmors
from opi.input.blocks.block_cpcm import AtomRadii, BlockCpcm, Radius
from opi.input.blocks.block_docker import BlockDocker
from opi.input.blocks.block_eda import BlockEda
from opi.input.blocks.block_elprop import BlockElprop
from opi.input.blocks.block_eprnmr import BlockEprnmr, NmrEquiv, NmrGroup, Nuclei, NucleiFlag
from opi.input.blocks.block_frag import BlockFrag, FragDefinition
from opi.input.blocks.block_freq import BlockFreq, HessList
from opi.input.blocks.block_geom import (
    BlockGeom,
    ConnectFragments,
    Constraint,
    Constraints,
    FragConstraint,
    Hybrid,
    Modify,
    ModifyInternal,
    Potential,
    Scan,
    TSMode,
)
from opi.input.blocks.block_goat import AtomList, BlockGoat
from opi.input.blocks.block_ice import BlockIce
from opi.input.blocks.block_irc import BlockIrc
from opi.input.blocks.block_loc import BlockLoc
from opi.input.blocks.block_mdci import BlockMdci
from opi.input.blocks.block_method import BlockMethod
from opi.input.blocks.block_mp2 import BlockMp2
from opi.input.blocks.block_neb import BlockNeb
from opi.input.blocks.block_output import BlockOutput
from opi.input.blocks.block_qmmm import BlockQmmm
from opi.input.blocks.block_rel import BlockRel
from opi.input.blocks.block_rocis import BlockRocis
from opi.input.blocks.block_scf import DIIS, SOSCF, BlockScf, Damp, Rotate, Shift, Stab, Trah
from opi.input.blocks.block_solvator import BlockSolvator
from opi.input.blocks.block_tddft import BlockTddft
from opi.input.blocks.block_xtb import BlockXtb
from opi.input.blocks.fragment import FragList, Fragment, Frags
from opi.input.blocks.geom_wrapper import Internal, Internals

__all__ = [
    "Block",
    "NumList",
    "IntGroup",
    "InputFilePath",
    "InputString",
    "BlockAutoCI",
    "NewBasis",
    "FragBasis",
    "FragAux",
    "FragEcp",
    "FragCabs",
    "FragAuxJ",
    "FragAuxJK",
    "FragAuxC",
    "BlockBasis",
    "BlockCasscf",
    "BlockCis",
    "BlockCosmors",
    "AtomRadii",
    "Radius",
    "BlockCpcm",
    "BlockDocker",
    "BlockEda",
    "BlockElprop",
    "NucleiFlag",
    "Nuclei",
    "NmrGroup",
    "NmrEquiv",
    "BlockEprnmr",
    "FragDefinition",
    "BlockFrag",
    "HessList",
    "BlockFreq",
    "BlockGeom",
    "ConnectFragments",
    "Constraint",
    "Constraints",
    "FragConstraint",
    "Hybrid",
    "Modify",
    "ModifyInternal",
    "Potential",
    "Scan",
    "TSMode",
    "AtomList",
    "BlockGoat",
    "BlockIce",
    "BlockIrc",
    "BlockLoc",
    "BlockMdci",
    "BlockMethod",
    "BlockMp2",
    "BlockNeb",
    "BlockOutput",
    "BlockQmmm",
    "BlockRel",
    "BlockRocis",
    "DIIS",
    "Shift",
    "Damp",
    "SOSCF",
    "Trah",
    "Stab",
    "Rotate",
    "BlockScf",
    "BlockSolvator",
    "BlockTddft",
    "BlockXtb",
    "Fragment",
    "FragList",
    "Frags",
    "Internal",
    "Internals",
]
