from unittest.mock import patch
# One of the errors we might get when we attempt
#  to connect to the db when the db is not ready
from psycopg2 import OperationalError as Psycopg2Error
# Django util which allows us to call a command by name
from django.core.management import call_command
from django.db.utils import OperationalError
# Created for unit tests
from django.test import SimpleTestCase

# Test custom manage.py commands.


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_to_be_ready(self, patched_check):
        """Test waiting for db ready"""
        patched_check.return_value = True
        # Executes the code in wait_for_db()
        call_command("wait_for_db")
        # With the mocked object 'check', check if
        #  it was called with the specified parametres (database="default")
        patched_check.assert_called_once_with(databases=["default"])

    # Replace the sleep function with a mocked object
    # representing the sleep function.
    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db to start" when getting OpertionalError"""
# Catching exceptions that could be raised.
# For the first 2 times, raise Psycopg2Error, after that,
#  the next 3 times, we raise OpertionalError.
# The reason why we raise different exceptions at
# different intervals is to deal with the stages it takes PostgreSQL to start.

# The first stage is when the PostgreSQL application hasn't
# even started yet and hence is not accepting connections:
#  in which case, you would get the Psycopg2 error.
# The second stage is when the app has started, and
#  its accepting connections, but it hasn't yet created the dev
# database/testing database which we want to raise,
# hence returning Django's OpertionalError.
# The number values are arbitary, and can change if not suitable.
        # On the 6th call, return True.

        patched_check.side_effect = [Psycopg2Error] \
         * 2 + [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        # Checks the check command was called 6 times.
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
