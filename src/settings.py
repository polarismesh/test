"""
Test project configuration file, you can modify the default configuration items or add custom configuration items here.
Use settings.get("CONFIG_NAME", "alternate_value") or settings.CONFIG_NAME to reference.
"""

# polaris console address
POLARIS_CONSOLE_ADDR = "127.0.0.1:8080"

# polaris server http restful api address
POLARIS_SERVER_HTTP_RESTFUL_API_ADDR = "127.0.0.1:8090"

# polaris server grpc service address
POLARIS_SERVER_GRPC_SERVICE_ADDR = "127.0.0.1:8091"

# polaris server grpc config address
POLARIS_SERVER_GRPC_CONFIG_ADDR = "127.0.0.1:8093"

# polaris server eureka service address
POLARIS_SERVER_EUREKA_SERVICE_ADDR = "127.0.0.1:8761"

# polaris server pushgateway address
POLARIS_SERVER_PUSHGATEWAY_ADDR = "127.0.0.1:9091"
