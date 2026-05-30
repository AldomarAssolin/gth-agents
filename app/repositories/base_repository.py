from app.extensions import db


class BaseRepository:
    model = None

    def list(self):
        return self.model.query.order_by(self.model.id.asc()).all()

    def get(self, entity_id: int):
        return db.session.get(self.model, entity_id)

    def create(self, **data):
        entity = self.model(**data)
        db.session.add(entity)
        db.session.commit()
        return entity

    def save(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
