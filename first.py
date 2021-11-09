from datetime import datetime
from marshmallow import Schema, fields, post_load
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.now()

    def __repr__(self):
        return f"username is : {self.name}"


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


# user = User(name="Monty", email="monty@python.org")
# schema = UserSchema()
# result = schema.dump(user)
user_data = {"name": "Ronnie", "email": "ronnie@stones.com"}
schema = UserSchema()
result = schema.dump(user_data)

print(result)