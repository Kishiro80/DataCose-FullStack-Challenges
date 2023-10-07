from schemas import createSchema, responseSchema, updateSchema
from app.models import User
from app.crud import CRUDBase

model = User
createSchema = createSchema
responseSchema = createSchema
updateSchema = createSchema
crud_fn = CRUDBase[model, createSchema,
                   responseSchema, updateSchema](model=model)

# Create a new user
new_row = createSchema(username="john_doe", email="john@example.com")
created_row = crud_fn.create(new_row)
print(created_row)

# Get a user by ID
user = crud_fn.get(id=1)
print(user)

# Get multiple users with pagination
users = crud_fn.get_multi(skip=0, limit=10)
print(users)

# Get multiple users with condition and pagination
users_with_condition = crud_fn.get_multi_with_condition(
    condition="User.username == 'john_doe'", skip=0, limit=10)
print(users_with_condition)

# Update a user
updated_user = crud_fn.update(
    db_obj=user, obj_in=updateSchema(username="jane_doe"))
print(updated_user)

# Delete a user
crud_fn.delete(db_obj=user)
