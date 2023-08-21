from uuid import UUID

from pydantic import BaseModel
from pydantic import Extra

from backend.models import Model


class PydanticBaseModel(BaseModel):
    class Config:
        orm_mode = True
        extra = Extra.forbid
        validate_all = True
        validate_assignment = True
        db_model: type[Model] = None
        exclude_for_update = {}

    def save_related_entities(self, db_model_instance):
        pass

    @classmethod
    def get_db_model(cls):
        try:
            return cls.Config.db_model
        except AttributeError:
            raise ValueError('Missing db_model in Config')

    def save(self, reload=True, output_validator=None):
        if output_validator is None:
            output_validator = getattr(self.Config, 'output_validator', self)
        db_model_instance = self.get_db_model()(**self.dict(exclude=self.Config.exclude_for_update))
        db_model_instance.save()
        self.save_related_entities(db_model_instance=db_model_instance)
        if reload:
            return output_validator.from_orm(db_model_instance)
        return self

    @classmethod
    def _get_model_by_id_or_404(cls, id):
        db_model = cls.get_db_model()

        item = db_model.not_deleted_query().filter(
            db_model.id == id
        ).first_or_404(
            description=f'{db_model.__name__} does not exist'
        )
        return item

    @classmethod
    def details(cls, id):
        item = cls._get_model_by_id_or_404(id)
        return cls.from_orm(item)

    @classmethod
    def update(cls, id: int | UUID, data: dict, partial: bool = False, output_validator: type[BaseModel] = None):
        if output_validator is None:
            output_validator = getattr(cls.Config, 'output_validator', cls)
        item = cls._get_model_by_id_or_404(id)
        if partial:
            original_data = cls.from_orm(item).dict(exclude=cls.Config.exclude_for_update)
            original_data.update(data)
            data = original_data
            del data['id']
        input_validator = cls(**data, id=id)
        data_for_update = input_validator.dict(exclude=cls.Config.exclude_for_update)
        item.update(**data_for_update)
        input_validator.save_related_entities(db_model_instance=item)
        return output_validator.from_orm(item)

    def patch(self, id: int | UUID, output_validator: type[BaseModel] = None):
        if output_validator is None:
            output_validator = getattr(self.Config, 'output_validator', self.__class__)
        item = self._get_model_by_id_or_404(id)
        item.update(**self.dict())
        if output_validator:
            return output_validator.from_orm(item)
        return self.from_orm(item)

    @classmethod
    def soft_delete(cls, id: int | UUID):
        item = cls._get_model_by_id_or_404(id=id)
        item.soft_delete()
