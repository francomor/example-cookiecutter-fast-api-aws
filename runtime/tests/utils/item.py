from runtime.src import crud
from runtime.src.db.session import db_session
from runtime.src.models.item import ItemCreate

from .user import create_random_user
from .utils import random_lower_string


def create_random_item(owner_id: int = None):
    if owner_id is None:
        user = create_random_user()
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, id=id)
    return crud.item.create(
        db_session=db_session, item_in=item_in, owner_id=owner_id
    )
