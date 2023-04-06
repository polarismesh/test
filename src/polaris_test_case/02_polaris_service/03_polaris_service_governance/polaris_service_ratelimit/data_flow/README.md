# Polaris-test

Auto test [Polaris](https://github.com/polarismesh/polaris)
with [Tencent/spring-cloud-tencent](https://github.com/Tencent/spring-cloud-tencent.git)
and [Tencent/QTAF](https://github.com/Tencent/QTAF.git).

---

## Introduction

该目录下测试用例集合串行执行，00_ratelimit_example_start.py 负责启动ratelimit consumer与provider，后续测试用例负责测试。

### 01_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:* | 自定义标签 test-key1 全匹配 test-value1 | 秒级 10秒5次 | 快速失败 |


