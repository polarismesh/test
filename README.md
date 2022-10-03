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

    export PYTHONPATH=${PYTHONPATH}:${polaris_test_dir}

其中 ${polaris_test_dir} 请替换为您当前polaris-test所在目录，例如：/root/polaris-test

### 5. 执行测试，详细配置见 [QTAF 说明文档](https://qta-testbase.readthedocs.io/zh/latest/testrun.html#)


#### 若您期望使用执行配置文件启动：

    python3 src/manage.py runtest --config-file test.json

#### 若您期望自定义执行用例启动-testpr：

    python3 src/manage.py runtest polaris_test_case/polaris_initial_login_check

