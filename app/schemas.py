from pydantic import BaseModel, Field

class CorporateMetricsIn(BaseModel):
    rd_spend: float = Field(..., gte=0, description="Research & Development expenditure array in INR")
    admin_cost: float = Field(..., gte=0, description="Administrative management cost overheads")
    marketing_spend: float = Field(..., gte=0, description="Localized marketing campaign asset allocation")

    class Config:
        json_schema_extra = {
            "example": {
                "rd_spend": 165349.20,
                "admin_cost": 136897.80,
                "marketing_spend": 471784.10
            }
        }
