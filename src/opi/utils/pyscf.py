"""
Optional interface to PySCF (https://pyscf.org).

PySCF is an optional dependency of OPI. See pyproject.toml for details.
"""

from opi.utils.optional import requires_optional

__all__ = ("requires_pyscf",)

requires_pyscf = requires_optional("pyscf", name="PySCF", package="pyscf")
"""
Decorator that raises an `ImportError` with a helpful message if PySCF is not installed.

Apply to any function or method that needs PySCF at runtime. The decorated function is expected
to import PySCF itself, locally, so that importing OPI never requires PySCF.
"""
