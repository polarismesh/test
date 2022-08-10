"""
Test project configuration file, you can modify the default configuration items or add custom configuration items here.
Use settings.get("CONFIG_NAME", "alternate_value") or settings.CONFIG_NAME to reference.
"""

# polaris console address
POLARIS_SERVER_ADDR = "119.91.218.43"

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
