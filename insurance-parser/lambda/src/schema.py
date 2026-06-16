from pydantic import BaseModel, Field
from typing import Optional


class ExtractedValue(BaseModel):
    """Wraps every extracted field with a confidence score and the raw text from the doc."""
    value: Optional[float | int | str | bool | list[str]] = None
    confidence: float = Field(ge=0.0, le=1.0)
    raw_text: Optional[str] = None  # what the doc actually said before normalisation


class SpecialExcess(BaseModel):
    peril: str
    amount: Optional[float] = None


class Subjectivity(BaseModel):
    text: str
    status: str = "outstanding"


class OptionalExtra(BaseModel):
    name: str
    additional_premium: Optional[float] = None


class PropertySection(BaseModel):
    buildings_sum_insured: ExtractedValue
    contents_machinery_sum_insured: ExtractedValue
    stock_sum_insured: ExtractedValue
    excess: ExtractedValue
    special_excesses: list[SpecialExcess] = []
    perils_included: ExtractedValue  # value will be list[str]
    perils_excluded: ExtractedValue  # value will be list[str]


class BusinessInterruptionSection(BaseModel):
    gross_profit_sum_insured: ExtractedValue
    indemnity_period_months: ExtractedValue
    excess: ExtractedValue


class LiabilitySection(BaseModel):
    employers_liability_limit: ExtractedValue
    public_liability_limit: ExtractedValue
    products_liability_limit: ExtractedValue
    products_basis: ExtractedValue  # 'each_and_every' | 'aggregate'
    excess: ExtractedValue


class OtherCoversSection(BaseModel):
    money_limit: ExtractedValue
    goods_in_transit_limit: ExtractedValue


class PremiumSection(BaseModel):
    net: ExtractedValue
    ipt: ExtractedValue
    ipt_rate: ExtractedValue
    gross: ExtractedValue
    instalments_available: ExtractedValue


class QuoteExtraction(BaseModel):
    # Top-level fields
    insurer_name: ExtractedValue
    quote_reference: ExtractedValue
    quote_date: ExtractedValue          # YYYY-MM-DD
    quote_valid_until: ExtractedValue   # YYYY-MM-DD or 'N days from issue'
    insured_name: ExtractedValue
    business_description: ExtractedValue
    turnover: ExtractedValue            # GBP number
    period_start: ExtractedValue        # YYYY-MM-DD
    period_end: ExtractedValue          # YYYY-MM-DD

    # Sections
    property: PropertySection
    business_interruption: BusinessInterruptionSection
    liability: LiabilitySection
    other_covers: OtherCoversSection
    premium: PremiumSection

    # Lists
    endorsements: list[str] = []
    exclusions: list[str] = []
    warranties: list[str] = []
    subjectivities: list[Subjectivity] = []
    optional_extras: list[OptionalExtra] = []
