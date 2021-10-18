from pydantic import BaseModel, Field

feature_names = [
    'alcohol',
    'malic_acid',
    'ash',
    'alcalinity_of_ash',
    'magnesium',
    'total_phenols',
    'flavanoids',
    'nonflavanoid_phenols',
    'proanthocyanins',
    'color_intensity',
    'hue',
    'od_of_diluted_wines',
    'proline'
]


class Features(BaseModel):
    alcohol: float = Field(
        ..., description="alchol", example=14.23
    )
    malic_acid: float = Field(
        ..., description="malic acid", example=1.71
    )
    ash: float = Field(
        ..., description="ash", example=2.43
    )
    alcalinity_of_ash: float = Field(
        ..., description="alcalinity of ash", example=15.6
    )
    magnesium: float = Field(
        ..., description="magnesium", example=127
    )
    total_phenols: float = Field(
        ..., description="total phenols", example=2.8
    )
    flavanoids: float = Field(
        ..., description="flavanoids", example=3.06
    )
    nonflavanoid_phenols: float = Field(
        ..., description="nonflavanoid_phenols", example=0.28
    )
    proanthocyanins: float = Field(
        ..., description='proanthocyanins', example=2.29
    )
    color_intensity: float = Field(
        ..., description='color_intensity', example=5.64
    )
    hue: float = Field(
        ..., description='hue', example=1.04
    )
    od_of_diluted_wines: float = Field(
        ..., description='od280/od315_of_diluted_wines', example=3.92
    )
    proline: float = Field(
        ..., description='proline', example=1.065
    )

class Prediction(BaseModel):
    label: float
    confidence: float

class HeartbeatResult(BaseModel):
    is_alive: bool

class StatusResult(BaseModel):
    is_alive: bool
