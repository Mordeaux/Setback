import json

import sqlalchemy.types as types

# Need to read up on SQLAlchemy mutability to make this work right
class Json(types.TypeDecorator):
    """This is a custom Type for SQLAlchemy which allows me to save JSON data
       and abstracts away the dumping and loading of this into the database."""

    impl = types.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)
