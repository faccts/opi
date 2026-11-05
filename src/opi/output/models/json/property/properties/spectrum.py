from pydantic import StrictBool, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictNonNegativeInt,
    StrictPositiveFloat,
    StrictPositiveInt,
)


class Spectrum(GetItem):
    """
    This class contains the information about calculated spectra like UVVis or ECD spectra

    Attributes
    ----------
    density_name: StrictStr | None, default = None
        Name of property with used theory
    temperature: StrictNonNegativeFloat | None, default = None
        Assumed temperature in the calculation
    method: StrictPositiveInt | None, default = None
        Method used in this calculation
    relcorrection: StrictPositiveInt | None, default = None
        Type of relativistic treatment in quasi degenerate perturbation theory in this calculation
    denstype: StrictNonNegativeInt | None, default = None
        Used density type in this calculation
    deritype: StrictNonNegativeInt | None, default = None
        Type of derived used in this calculation
    denslevel: StrictNonNegativeInt | None, default = None
        Source of density
    representation: StrictStr | None, default = None
        Used representation (passible Unknown, Length, Velocity)
    pointgroup: StrictStr | None, default = None
        Pointgroup of the molecule
    ntrans: StrictNonNegativeInt | None, default = None
        Number of transition states modeled in the calculation
    dohighermoments: StrictBool | None, default = None
        Are higher moments supposed to be used
    states: list[tuple[StrictNonNegativeInt, StrictNonNegativeInt, StrictPositiveInt, StrictNonNegativeInt]]| None, default = None
        Contains the initial and final states
    multiplicities: list[tuple[StrictPositiveFloat, StrictPositiveFloat]] | None, default = None
        Contains the multiplicity of the initial and final state
    excitationenergies: list[list[StrictFiniteFloat]] | None, default = None
        One row per transition, see `AbsorptionSpectrum` and `EcdSpectrum` for the columns
    """

    density_name: StrictStr | None = None
    temperature: StrictNonNegativeFloat | None = None
    method: StrictPositiveInt | None = None
    relcorrection: StrictPositiveInt | None = None
    denstype: StrictNonNegativeInt | None = None
    deritype: StrictNonNegativeInt | None = None
    denslevel: StrictNonNegativeInt | None = None
    representation: StrictStr | None = None
    pointgroup: StrictStr | None = None
    ntrans: StrictNonNegativeInt | None = None
    dohighermoments: StrictBool | None = None
    states: (
        list[
            tuple[
                StrictNonNegativeInt,
                StrictNonNegativeInt,
                StrictPositiveInt,
                StrictNonNegativeInt,
            ]
        ]
        | None
    ) = None
    multiplicities: list[tuple[StrictPositiveFloat, StrictPositiveFloat]] | None = None
    excitationenergies: list[list[StrictFiniteFloat]] | None = None

    def _column(self, index: int) -> list[float] | None:
        """
        Extract one column of `excitationenergies`, i.e., one quantity for all transitions.

        Parameters
        ----------
        index: int
            Index of the column

        Returns
        -------
        list[float] | None
            The requested column, None if the output contains no excitation energies.
        """
        if self.excitationenergies is None:
            return None
        return [transition[index] for transition in self.excitationenergies]

    def _complex_vectors(self, start: int) -> list[tuple[complex, complex, complex]] | None:
        """
        Extract a complex vector (x, y, z) for all transitions from `excitationenergies`.

        ORCA stores each component as a pair of real and imaginary part, i.e., the six columns
        starting at `start` hold Re(x), Im(x), Re(y), Im(y), Re(z) and Im(z).

        Parameters
        ----------
        start: int
            Index of the column holding the real part of the x component

        Returns
        -------
        list[tuple[complex, complex, complex]] | None
            One (x, y, z) vector per transition, None if the output contains no excitation
            energies.
        """
        if self.excitationenergies is None:
            return None
        return [
            (
                complex(row[start], row[start + 1]),
                complex(row[start + 2], row[start + 3]),
                complex(row[start + 4], row[start + 5]),
            )
            for row in self.excitationenergies
        ]

    @property
    def energies_ev(self) -> list[float] | None:
        """
        The excitation energies of all transitions in eV.

        Shortcut for the first column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(0)

    @property
    def energies_cm(self) -> list[float] | None:
        """
        The excitation energies of all transitions in cm**-1.

        Shortcut for the second column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(1)

    @property
    def wavelengths_nm(self) -> list[float] | None:
        """
        The wavelengths of all transitions in nm.

        Shortcut for the third column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(2)


class AbsorptionSpectrum(Spectrum):
    """
    This class contains the information about a calculated electronic absorption (UV/Vis)
    spectrum.

    Each row of `excitationenergies` describes one transition and holds the excitation energy in
    eV and in cm**-1, the wavelength in nm, the oscillator strength, the squared transition
    moment in au, and the real and imaginary parts of the x, y and z components of the transition
    moment in au. The properties of this class give direct access to these columns.

    In the length representation the transition moment is the electric transition dipole moment,
    in the velocity representation it is the transition velocity dipole moment, see
    `representation`.
    """

    @property
    def oscillator_strengths(self) -> list[float] | None:
        """
        The oscillator strengths of all transitions (dimensionless).

        Shortcut for the fourth column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(3)

    @property
    def transition_moments_squared(self) -> list[float] | None:
        """
        The squared absolute values of the transition moments of all transitions in au.

        Shortcut for the fifth column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(4)

    @property
    def transition_moments(self) -> list[tuple[complex, complex, complex]] | None:
        """
        The (x, y, z) components of the transition moments of all transitions in au.

        The components are complex numbers, assembled from the pairs of real and imaginary parts
        in the last six columns of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._complex_vectors(5)


class EcdSpectrum(Spectrum):
    """
    This class contains the information about a calculated electronic circular dichroism (ECD)
    spectrum.

    Each row of `excitationenergies` describes one transition and holds the excitation energy in
    eV and in cm**-1, the wavelength in nm, the rotatory strength in 1e-40 cgs, and the real and
    imaginary parts of the x, y and z components of the magnetic transition dipole moment in au.
    The properties of this class give direct access to these columns.
    """

    @property
    def rotatory_strengths(self) -> list[float] | None:
        """
        The rotatory strengths of all transitions in 1e-40 cgs (esu**2 cm**2).

        Shortcut for the fourth column of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._column(3)

    @property
    def magnetic_transition_moments(self) -> list[tuple[complex, complex, complex]] | None:
        """
        The (x, y, z) components of the magnetic transition dipole moments of all transitions in
        au.

        The components are complex numbers, assembled from the pairs of real and imaginary parts
        in the last six columns of `excitationenergies`. None if the output contains no
        excitation energies.
        """
        return self._complex_vectors(4)
