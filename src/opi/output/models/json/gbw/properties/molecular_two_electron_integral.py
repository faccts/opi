from pydantic import Field

from opi.output.models.base.get_item import GetItem
from opi.output.models.json.gbw.properties.two_electron_integral_element import (
    TwoElectronIntegralElement,
)


class MOTwoElectronIntegral(GetItem):
    """
    This class contains the information about two electron integrals in MO basis

    Attributes
    ----------
    alpha_alpha : list[TwoElectronIntegralElement]
        Two electron integral over alpha/alpha MOs
    alpha_beta : list[TwoElectronIntegralElement]
        Two electron integral over alpha/beta MOs
    beta_alpha : list[TwoElectronIntegralElement]
        Two electron integral over beta/alpha MOs
    beta_beta : list[TwoElectronIntegralElement]
        Two electron integral over beta/beta MOs
    """

    alpha_alpha: list[TwoElectronIntegralElement] | None = Field(default=None, alias="alpha/alpha")
    alpha_beta: list[TwoElectronIntegralElement] | None = Field(default=None, alias="alpha/beta")
    beta_alpha: list[TwoElectronIntegralElement] | None = Field(default=None, alias="beta/alpha")
    beta_beta: list[TwoElectronIntegralElement] | None = Field(default=None, alias="beta/beta")
