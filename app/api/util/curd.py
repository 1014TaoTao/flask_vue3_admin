from marshmallow import Schema

from app.plugin.init_sqlalchemy import db



def auto_model_jsonify(data, model: db.Model):
    def get_model():
        return model

    class BaseSchema(Schema):
        class Meta:
            model = get_model()
            
    base_schema = BaseSchema()  # 使用自定义的Schema类生成序列化类
    output = base_schema.dump(data)  # 序列化数据
    return output

def model_to_dict(schema: Schema, data):
    common_schema = schema()  # 使用自定义的Schema类生成序列化类
    output = common_schema.dump(data)  # 序列化数据
    return output

def dict_to_model(model: db.Model, data: dict):
    for key, value in data.items():
        setattr(model, key, value)
    return model


def get_one_by_id(model: db.Model, id):
    return model.query.filter_by(id=id).first()


def delete_one_by_id(model: db.Model, id):
    r = model.query.filter_by(id=id).delete()
    db.session.commit()
    return r
