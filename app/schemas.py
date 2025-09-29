from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(allow_none=True)
    completed = fields.Bool(allow_none=False)
    # created_at = fields.DateTime(dump_only=True)
    # updated_at = fields.DateTime(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)

class TaskCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    completed = fields.Bool(allow_none=False)

class TaskUpdateSchema(TaskCreateSchema):
    pass


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserOutSchema(Schema):
    username = fields.Str(required=True)

class TokenSchema(Schema):
    access_token =  fields.Str(required=True)
    token_type =  fields.Str(required=True)