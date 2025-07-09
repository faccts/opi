from typing import Any, Callable, Literal, Union

from pydantic import BaseModel, Field

from opi.input.blocks import Block
from opi.input.simple_keywords import Solvent

__all__ = ("AtomRadii", "Radius", "BlockCpcm")


class AtomRadii(BaseModel):
    """
    Class to model `atomradii` attribute in `BlockCpcm`.

    Attributes
    -----------
    n: int
        Number of atom for which radius is defined
    radius: float
        Radius(in Angstrom)
    """

    n: int = Field(gt=0, le=118)
    radius: float = Field(gt=0.0)

    def __str__(self) -> str:
        return f"AtomRadii({str(self.n)}, {str(self.radius)})"


class Radius(BaseModel):
    """
    Class to model `radius` and `radii` attributes in `BlockCpcm`.

    Attributes
    ----------
    n: int
        Atomic number for which radius is to be defined.
    value: float
        Atomic radius(in Angstrom)

    """

    n: int = Field(gt=0, le=118)
    value: float = Field(gt=0.0)

    def __str__(self) -> str:
        return f"[{self.n}] {str(self.value)}"


class BlockCpcm(Block):
    """Class to model %cpcm block in ORCA"""

    _name: str = "cpcm"
    epsilon: float | None = None  # Dielectric constant
    xfeps: float | None = None  # X parameter for the feps scaling function
    num_leb: int | None = None  # Lebedev points for the Gaussian charge scheme
    scale_gauss: float | None = (
        None  # Scaling factor for the atomic radii in the Gaussian charge scheme
    )
    refrac: float | None = None  # Refractive index
    rsolv: float | None = None  # Solvent probe radius
    radii: Radius | None = None  # radius [n], give a vector of radii
    radius: Radius | None = None  # radius [n], give a vector of radii
    rmin: float | None = None  # Minimal GEPOL sphere radius
    pmin: float | None = None  # Minimal distance between two surface points
    rsolv_sas: float | None = None  # Solvent probe radius for sas
    ndiv: int | None = None  # Maximum depth for recursive sphere generation
    cds_cpcm: int | None = None  # Use of the GVDW_nel or GSES_nel scheme
    cpcmccm: int | None = None  # Coupled-cluster/C-PCM scheme
    cut_swf: float | None = (
        None  # Cutoff for the switching function Only valid for the Gaussian charge scheme
    )
    cut_area: float | None = (
        None  # Cutoff for the area of a surface segment in a.u. Only valid for the Gaussian charge scheme
    )
    thresh_h: float | None = (
        None  # Threshold for the charge density on a hydrogen atom in charges/Å^2 (isodensity scheme)
    )
    thresh_noth: float | None = (
        None  # Threshold for the charge density on non-hydrogen atoms in charges/Å^2 (isodensity scheme)
    )
    draco: bool | None = None  # enable dynamic charge scaling of radii (draco)
    dracogridfollow: bool | None = (
        None  # Adapt grid to the new radii in geometry optimizations within the DRACO scheme
    )
    cavityfile: bool | None = (
        None  # read the coordinates of the C-PCM charges from an external file
    )
    fepstype: Literal["cpcm", "cosmo"] | None = None  # Epsilon function type: cpcm, cosmo
    surfacetype: Literal["gepol_ses", "gepol_sas", "vdw_gaussian", "gepol_ses_gaussian"] | None = (
        None  # Cavity surface
    )
    draco_charges: Literal["eeq", "ceh"] | None = None  # Charge model for draco
    newradii: bool | None = None  # Use new atomic radii
    smd: bool | None = None  # Use SMD
    smdold: bool | None = None  # Use the old SMD
    smd18: bool | None = None  # Use updated radii for some elements
    aqueous: bool | None = None  # SMD: Is the solvent aqueous?
    soln: float | None = None  # SMD: index of refraction at optical frequencies at 293 K
    soln25: float | None = None  # SMD: index of refraction at optical frequencies at 298 K
    sola: float | None = None  # SMD: Abraham's hydrogen bond acidity
    solb: float | None = None  # SMD: Abraham's hydrogen bond basicity
    solg: float | None = None  # SMD: relative macroscopic surface tension
    solc: float | None = (
        None  # SMD: aromaticity, fraction of non-hydrogenic solvent atoms that are aromatic carbon atoms
    )
    solh: float | None = (
        None  # SMD: electronegative halogenicity, fraction of non-hydrogenic # solvent atoms that are F, Cl, or Br
    )
    cosmorscalc: bool | None = None  # COSMORS keyword
    useriifpossible: bool | None = None  # Use RI when possible?
    useanalyticonrebuild: bool | None = (
        None  # full analytic build upon restart of the direct SCF method
    )
    vpottype: int | None = None  # Special potential options
    vpotopt: int | None = None  # Special potential options
    vopt: Literal["v_analytic", "v_numeric", "v_multipole", "v_ri"] | None = (
        None  # Special potential options
    )
    pcfocktype: int | None = None  # Special potential options
    pffockopt: int | None = None  # Special potential options
    fockopt: int | None = None  # Special potential options
    fopt: Literal["f_analytic", "f_numeric", "f_multipole", "f_ri"] | None = (
        None  # Special potential options
    )
    atomradii: AtomRadii | None = None
    solvent: Solvent | None = None  # specifies solvent by name
    smdsolvent: Solvent | None = None

    def format_orca(self) -> str:
        special_handlers: dict[str, Callable[[Any], Union[str, None]]] = {
            "aftercoord": lambda v: None,  # Skip this field
            "radii": lambda v: f"    radii{str(v)}",
            "radius": lambda v: f"    radius{str(v)}",
            "atomradii": lambda v: f"    {str(v)}",
            "smdsolvent": lambda v: f'    smdsolvent "{str(v).lower()}"',
            "solvent": lambda v: f'    solvent "{str(v).lower()}"',
        }
        s = f"%{self.name}\n"
        for key, value in self.__dict__.items():
            if value is not None:
                if key in special_handlers:
                    line = special_handlers[key](value)
                    if line:
                        s += line + "\n"
                else:
                    s += f"    {key} {str(value).lower()}\n"
        s += "end"

        return s
