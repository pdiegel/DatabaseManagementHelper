import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="DatabaseManager.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M",
    force=True,
)
