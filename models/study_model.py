import dataclasses
from datetime import datetime

from core.base_model import BaseModel

@dataclasses.dataclass(kw_only=True, frozen=True)
class StudyModel(BaseModel):
    user_id: str
    start_time: datetime
    end_time: datetime
    total_min: int
