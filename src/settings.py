"""
Test project configuration file, you can modify the default configuration items or add custom configuration items here.
Use settings.get("CONFIG_NAME", "alternate_value") or settings.CONFIG_NAME to reference.
"""

# polaris console address
POLARIS_SERVER_ADDR = "10.0.3.58"
# polaris console root username
POLARIS_SERVER_USERNAME = "100024759858"

# polaris console root password
POLARIS_SERVER_PASSWORD = "polarismesh@2022"

# polaris console token owner, default is polaris
POLARIS_SERVER_TOKEN_OWNER = "100020616957"

# polaris console address
POLARIS_CONSOLE_ADDR = "{POLARIS_SERVER_ADDR}:8080".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# polaris server http restful api address
POLARIS_SERVER_HTTP_RESTFUL_API_ADDR = "{POLARIS_SERVER_ADDR}:8090".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# polaris server grpc service address
POLARIS_SERVER_GRPC_SERVICE_ADDR = "{POLARIS_SERVER_ADDR}:8091".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# polaris server grpc config address
POLARIS_SERVER_GRPC_CONFIG_ADDR = "{POLARIS_SERVER_ADDR}:8093".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# polaris server eureka service address
POLARIS_SERVER_EUREKA_SERVICE_ADDR = "{POLARIS_SERVER_ADDR}:8761".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# polaris server pushgateway address
POLARIS_SERVER_PUSHGATEWAY_ADDR = "{POLARIS_SERVER_ADDR}:9091".format(POLARIS_SERVER_ADDR=POLARIS_SERVER_ADDR)

# tencent kona jdk version, default 11
# use kona jdk 17 to test spring cloud tencent 2022
# use kona jdk 11 to test spring cloud tencent 2021/2020
POLARIS_TEST_SCT_KONA_JDK_VERSION = 11

# spring cloud tencent version, default 2021
# use kona jdk 17 to test spring cloud tencent 2022
# use kona jdk 11 to test spring cloud tencent 2021/2020
POLARIS_TEST_SCT_EXAMPLE_VERSION = 2021
