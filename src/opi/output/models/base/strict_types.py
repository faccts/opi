from pydantic import Field, FiniteFloat, NonNegativeInt, PositiveInt, Strict
from typing import Union
from typing_extensions import Annotated

StrictPositiveInt = Annotated[PositiveInt, Strict()]

StrictNonNegativeInt = Annotated[NonNegativeInt, Strict()]

StrictFiniteFloat = Annotated[FiniteFloat, Strict()]

StrictPositiveFloat = Annotated[FiniteFloat, Strict(), Field(gt=0)]

StrictNonNegativeFloat = Annotated[FiniteFloat, Strict(), Field(ge=0)]

StrictNegativeFloat = Annotated[FiniteFloat, Strict(), Field(lt=0)]

StrictPositiveFloatOrMinusOne = Annotated[
    Union[
        Annotated[FiniteFloat, Strict(), Field(gt=0)],  # Positive float
        Annotated[FiniteFloat, Strict(), Field(ge=-1, le=-1)]   # Exactly -1
    ],
    Field(description="Positive float or -1")
]