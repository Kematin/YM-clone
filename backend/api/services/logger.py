from loguru import logger


def create_logger():
    logger.add(
        "logs/debug.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="100 KB",
        compression="zip",
    )
    logger.info("Create logger")


if __name__ == "__main__":
    logger.debug("Add data to db.")
    logger.info("Create new user 'user'.")
    logger.warning("Forbidden to create new item.")
    logger.error("Fn 'create_new_item' was broken by error - 'error'.")
    logger.critical("Api was broken with error 'error'.")
