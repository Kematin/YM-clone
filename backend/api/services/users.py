from typing import List

from database.connection import Base
from loguru import logger
from models.users import UpdateUser


@logger.catch
def check_username(user_data: UpdateUser, db_users: List[Base] | None) -> True:
    """Function that checks the received username for reuse in the database

    Args:
        user_data (UpdateUser): json loads data
        db_users (List[Base] | None): query from database

    Returns:
        False: username already in use.
        True: username unique.
    """

    user_data = user_data.model_dump()
    new_username = user_data.get("username", None)

    if new_username is None:
        return True

    for db_user in db_users:
        if db_user.username == new_username:
            return False

    return True
