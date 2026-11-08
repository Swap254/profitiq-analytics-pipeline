from typing import List

from pydantic import BaseModel, Field


class CorporateMetricsIn(BaseModel):
    rd_spend: float = Field(
        ...,
        ge=0,
        description="Research & Development expenditure in INR",
    )

    admin_cost: float = Field(
        ...,
        ge=0,
        description="Administrative management cost in INR",
    )

    marketing_spend: float = Field(
        ...,
        ge=0,
        description="Marketing expenditure in INR",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rd_spend": 165349.20,
                "admin_cost": 136897.80,
                "marketing_spend": 471784.10,
            }
        }


class BatchCorporateMetricsIn(BaseModel):
    records: List[CorporateMetricsIn] = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="List of corporate financial records",
    )