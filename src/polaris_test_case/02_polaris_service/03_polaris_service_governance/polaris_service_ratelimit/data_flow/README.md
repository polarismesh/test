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

### 02_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 全匹配 /business/info | 请求头(HEADER) test-header-key1 包含 test-header-value1 | 秒级 10秒5次 | 快速失败 |

### 03_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 正则匹配 /business/.* | 请求参数(HEADER) test-header-key1 不包含 test-header-value1 | 秒级 10秒5次 | 快速失败 |

### 04_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 不包含 /business/info | 方法(METHOD) $method 不等于 GET | 秒级 10秒5次 | 快速失败 |

### 05_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 包含 /business/info | 主调服务 default 正则匹配 RateLimitCaller.* | 秒级 10秒5次 | 快速失败 |

### 06_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |               目标服务               |             请求流量画像              | 限流条件 | 限流方案 |
|:----:|:--------------------------------:|:-------------------------------:|:----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 不等于 /business/info | 主调IP(METHOD) $caller_ip 正则匹配 ((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})(\\.((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})){3} | 秒级 10秒5次 | 快速失败 |
