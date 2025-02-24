from app.plugin.init_sqlalchemy import db


def model_to_dict(s: type, m: db.Model) -> dict:
    return s().dump(m)


def dict_to_model(s: type, d: dict) -> db.Model:
    return s().load(d)
