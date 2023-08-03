#!/usr/bin/env python3
"""
Personal data
"""
import re
import logging
import os
import mysql.connector
from typing import List


"""Define the PII_FIELDS tuple constant"""
PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for f in fields:
        message = re.sub(rf"{f}=(.*?)\{separator}",
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Implementing a logger.
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Implement db conectivity
    """
    db_psw = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_username,
        password=db_psw)
    return conn


def main():
    """Retrieve all rows from users table and display them with filtering."""
    logger = get_logger()
    db = get_db()

    if db is None:
        logger.error("Error connecting to the database")
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    logger.info("Filtered data:")
    for row in rows:
        filtered_row = []
        for field in PII_FIELDS:
            filtered_row.append(f"{field}={logger.REDACTION}")
        filtered_row.append(f"ip={row['ip']}")
        filtered_row.append(f"last_login={row['last_login']}")
        filtered_row.append(f"user_agent={row['user_agent']}")
        logger.info(" ".join(filtered_row))


if __name__ == "__main__":
    main()
