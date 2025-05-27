import dataclasses

from bson import ObjectId


@dataclasses.dataclass(kw_only=True, frozen=True)
class BaseModel:
    _id: ObjectId = dataclasses.field(default_factory=ObjectId)

    @property
    def id(self) -> ObjectId | None:
        return self._id
