import dataclasses
from datetime import datetime

from core.base_model import BaseModel


@dataclasses.dataclass(kw_only=True, frozen=True)
class AttendModel(BaseModel):
    user_id: str
    attend_time: datetime
