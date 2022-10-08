from testbase.conf import settings
from testbase.testcase import TestCase


class InitialLoginCheck(TestCase):
    """
    Used to test the editing of the basic information of the Polaris namespace.
    For the test cases related to editing authorization, see xxx.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Design
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.start_step("")
        POLARIS_SERVER_ADDR = settings.get("POLARIS_SERVER_ADDR", "127.0.0.1:8080")

        # ===========================
        self.log_info("hello")
