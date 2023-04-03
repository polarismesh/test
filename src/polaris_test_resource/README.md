# Polaris-test

Auto test [Polaris](https://github.com/polarismesh/polaris)
with [Tencent/spring-cloud-tencent](https://github.com/Tencent/spring-cloud-tencent.git)
and [Tencent/QTAF](https://github.com/Tencent/QTAF.git).

---

## Introduction

### polaris-go-demo

可执行文件 provider 由 [polaris-go](https://github.com/polarismesh/polaris-go) 下 examples/quickstart/provider 编译而来。

### eureka-demo

可执行文件 consumer/provider jar包 由 [polaris-examples](https://github.com/polarismesh/examples) 下
servicediscovery/eureka/eureka-java 编译而来。

### tencent-kona

11/17 release 见 [tencent-kona-11](https://github.com/Tencent/TencentKona-11/releases)
和 [tencent-kona-17](https://github.com/Tencent/TencentKona-17/releases)

### spring-cloud-tencent-demo

可执行文件 jar包
由 [spring-cloud-tencent-examples](https://github.com/Tencent/spring-cloud-tencent/tree/2021.0/spring-cloud-tencent-examples)
编译而来。 您可以自行选择对应的版本进行编译测试，现在自动运行的polaris质量门禁流水线中，默认使用2021版本的jar包进行测试。

