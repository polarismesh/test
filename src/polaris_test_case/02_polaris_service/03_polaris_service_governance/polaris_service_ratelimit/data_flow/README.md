# Polaris-test

Auto test [Polaris](https://github.com/polarismesh/polaris)
with [Tencent/spring-cloud-tencent](https://github.com/Tencent/spring-cloud-tencent.git)
and [Tencent/QTAF](https://github.com/Tencent/QTAF.git).

---

## Introduction

该目录下测试用例集合串行执行，00_ratelimit_example_start.py 负责启动ratelimit consumer与provider，后续测试用例负责测试。

### 01_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |  目标服务<div style="width:500px">   | 请求流量画像<div style="width:600px"> | 限流条件<div style="width:400px"> | 限流方案<div style="width:400px"> |
|:----:|:--------------------------------:|:-------------------------------:|:-----------------------------:|:-----------------------------:|
| 单机限流 | default:RateLimitCalleeService:* | 自定义标签 test-key1 全匹配 test-value1 |             10秒5次             |             快速失败              |

### 02_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |            目标服务<div style="width:500px">             |                    请求流量画像<div style="width:600px">                    | 限流条件<div style="width:400px">  | 限流方案<div style="width:400px"> |
|:----:|:----------------------------------------------------:|:---------------------------------------------------------------------:|:-----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 全匹配 /business/info | 请求头(HEADER) test-header-key1 包含 test-header-value1,test-header-value2 | 10秒5次 | 快速失败 |

### 03_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |            目标服务<div style="width:500px">            |   请求流量画像<div style="width:600px">    | 限流条件<div style="width:400px">  | 限流方案<div style="width:400px"> |
|:----:|:---------------------------------------------------:|:------------------------------------:|:-----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 正则匹配 /business/.* | 请求参数(QUERY) value1 不包含 value1,value2 | 10秒5次 | 快速失败 |

### 04_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |                    目标服务<div style="width:500px">                     | 请求流量画像<div style="width:600px"> | 限流条件<div style="width:400px">  | 限流方案<div style="width:400px"> |
|:----:|:--------------------------------------------------------------------:|:-------------------------------:|:-----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 不包含 /business/info,/business/info2 |   方法(METHOD) $method 不等于 POST   | 10秒5次 | 快速失败 |

### 05_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |                        目标服务<div style="width:500px">                         |   请求流量画像<div style="width:600px">   | 限流条件<div style="width:400px">  | 限流方案<div style="width:400px"> |
|:----:|:----------------------------------------------------------------------------:|:-----------------------------------:|:-----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 包含 /business/info,/business/info/webclient | 主调服务 default 正则匹配 RateLimitCaller.* | 10秒5次 | 快速失败 |

### 06_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |            目标服务<div style="width:500px">             |                                               请求流量画像<div style="width:600px">                                               | 限流条件<div style="width:400px">  | 限流方案<div style="width:400px"> |
|:----:|:----------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------:|:-----:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 不等于 /business/info | 主调IP $caller_ip 正则匹配 ((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})(\\.((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})){3} | 10秒5次 | 快速失败 |

### 07_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |            目标服务<div style="width:500px">            |                                               请求流量画像<div style="width:600px">                                               |      限流条件<div style="width:400px">       | 限流方案<div style="width:400px"> |
|:----:|:---------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------:|:---------------:|:----:|
| 单机限流 | default:RateLimitCalleeService:接口 等于 /business/info | 主调IP $caller_ip 正则匹配 ((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})(\\.((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})){3} | 10秒10次 + 20秒15次 | 快速失败 |

### 08_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |  目标服务<div style="width:500px">   |                                               请求流量画像<div style="width:600px">                                               | 限流条件<div style="width:400px"> |     限流方案<div style="width:400px">      |
|:----:|:--------------------------------:|:---------------------------------------------------------------------------------------------------------------------------:|:-----------------------------:|:-------------:|
| 单机限流 | default:RateLimitCalleeService:* | 主调IP $caller_ip 正则匹配 ((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})(\\.((2(5[0-5]&#124;[0-4]\\d))&#124;[0-1]?\\d{1,2})){3} |             1秒7次              | 匀速排队:最大排队时长2s |

### 09_ratelimit_rule_scene_check

该用例测试场景为：

| 限流类型 |  目标服务<div style="width:500px">   | 请求流量画像<div style="width:600px"> | 限流条件<div style="width:200px"> | 限流方案<div style="width:200px"> | 启用状态<div style="width:250px"> | 优先级<div style="width:100px"> |
|:----:|:--------------------------------:|:-------------------------------:|:-----------------------------:|:-----------------------------:|:-----------------------------:|:----------------------------:|
| 单机限流 | default:RateLimitCalleeService:* | 自定义标签 test-key1 全匹配 test-value1 |             1秒7次              |         匀速排队:最大排队时长2s         |          启用->禁用->启用           |             高优先级             |
| 单机限流 | default:RateLimitCalleeService:* | 自定义标签 test-key1 全匹配 test-value1 |             10秒5次             |             快速失败              |              启用               |             低优先级             |
