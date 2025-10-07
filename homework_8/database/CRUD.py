from sqlalchemy import select


from .model import db

def reset_db():
    db.drop_all()
    db.create_all()

def create_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    db.session.commit()
    return instance

def get_instance(model, instance_id):
    return db.session.get(model, instance_id)

def list_instances(model):
    return db.session.scalars(select(model).order_by(model.id)).all()

def update_instance(model, instance_id, **kwargs):
    instance = get_instance(model, instance_id)
    if not instance:
        return False
    for key, value in kwargs.items():
        setattr(instance, key, value)
    db.session.commit()
    return True

def delete_instance(model, instance_id):
    instance = get_instance(model, instance_id)
    if not instance:
        return False
    db.session.delete(instance)
    db.session.commit()
    return True

