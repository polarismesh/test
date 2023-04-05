from testbase.conf import settings

from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class PolarisDependencyInitCheck(PolarisTestCase):
    """
    Used to init polaris dependencies.

    """
    owner = "atom"
    status = PolarisTestCase.EnumStatus.Ready
    priority = PolarisTestCase.EnumPriority.Normal
    timeout = 15

    def run_test(self):
        # ===========================
        self.start_step("Init jdk 11 and 17.")
        self.get_kona_jdk(11)
        self.get_kona_jdk(17)
        # ===========================
        self.start_step("Init Spring Cloud Tencent %s" % settings.POLARIS_TEST_SCT_EXAMPLE_VERSION)
        self.get_spring_cloud_tencent_example()


if __name__ == '__main__':
    PolarisDependencyInitCheck().debug_run()
