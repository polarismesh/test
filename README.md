# Polaris-test

Auto test [Polaris](https://github.com/polarismesh/polaris)
with [Tencent/spring-cloud-tencent](https://github.com/Tencent/spring-cloud-tencent.git)
and [Tencent/QTAF](https://github.com/Tencent/QTAF.git).

---

## Quickstart

### 0. 启动 Polaris-server，详见[北极星单机版安装](https://polarismesh.cn/zh/doc/%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/%E5%AE%89%E8%A3%85%E6%9C%8D%E5%8A%A1%E7%AB%AF/%E5%AE%89%E8%A3%85%E5%8D%95%E6%9C%BA%E7%89%88.html#%E5%8D%95%E6%9C%BA%E7%89%88%E5%AE%89%E8%A3%85)

### 1. 安装 QTAF依赖

    pip3 install qtaf

### 2. 修改用例配置文件 src/settings.py

指定POLARIS_SERVER_ADDR为你的北极星server地址

### 3. 修改用例执行配置文件 src/runtest_config.json

详细配置说明见 [QTAF 说明文档](https://qta-testbase.readthedocs.io/zh/latest/testrun.html#section-12)

配置文件中已为您默认指定了 polaris_test_case.polaris_initial_login_check 基础测试用例，用于检查初始密码登录。


### 4. 指定 Python3执行目录（可选）

    export PYTHONPATH=$PYTHONPATH:${polaris_test_dir}

其中 ${polaris_test_dir} 请替换为您当前polaris-test所在目录，例如：/root/test

### 5. 进入src目录下执行测试，详细配置见 [QTAF 说明文档](https://qta-testbase.readthedocs.io/zh/latest/testrun.html#)


#### 若您期望使用执行配置文件启动（此处将会执行当前支持的所有测试用例场景，采用并发线程执行，并发数5，请注意执行机以及server端负载。）：

    python3 manage.py runtest --config-file runtest_config.json


#### 若您期望自定义执行用例启动：

    python3 manage.py runtest polaris_test_case.polaris_initial_login_check

### 6. 基于 Spring CLoud Tencent 的服务治理相关测试说明
#### 若您期望执行Spring cloud Tencent相关用例，需要在您的执行机上提前安装好maven环境。我们会在测试时即时编译相关的example包。
#### 您也可以提前编译好对应的example包上传到对应的测试版本目录下，如：

    .
    ├── discovery-callee-service-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── discovery-caller-service-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── polaris-circuitbreaker-callee-service-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── polaris-circuitbreaker-callee-service2-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── polaris-circuitbreaker-feign-example-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── polaris-config-example-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── ratelimit-callee-service-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── router-callee-service1-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── router-callee-service2-1.11.0-2020.0.6-SNAPSHOT.jar
    ├── router-caller-service-1.11.0-2020.0.6-SNAPSHOT.jar
    └── spring-cloud-tencent 【若检测到当前目录下不包含上述依赖的测试example jar包，polaris-test会即时clone sct然后编译。】

#### 测试所依赖的example包括：

    polaris-discovery-example
    polaris-config-example
    polaris-circuitbreaker-example
    polaris-ratelimit-example
    polaris-router-example

#### 您可以直接在对应版本的 [SCT DEMO](https://github.com/Tencent/spring-cloud-tencent/tree/2021.0/spring-cloud-tencent-examples) 下编译获得。
