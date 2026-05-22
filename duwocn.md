# 读我 CN：目录导览

这份文档给第一次进仓库的人看。它不讲项目历史细节，只回答一个问题：
“我现在看到这些文件夹，到底该进哪里、别碰哪里？”

## 先看哪几个

- `README.md`：当前 new 版状态总览，包含 103 个 case-bank 包、46/53 两个交付口径。
- `docs/case-bank/README.md`：case-bank 的正式入口，解释包状态、ledger 和打包命令。
- `docs/case-bank/cases/`：真正的 benchmark case 包都在这里。
- `duwocn.md`：就是本文，给 human 的中文地图。

## 一级文件夹

### `.github/`

GitHub 自动化配置。现在主要看 `.github/workflows/`，里面是 CI 或未来自动检查入口。
普通读库、打包、审 case 时基本不用进。

### `.uv-cache/`

`uv` 的本地依赖缓存。本地跑复现或测试时会产生，不能当作项目资料，也不要提交。

### `.uv-python/`

`uv` 下载的本地 Python 解释器。本地运行环境产物，不是源码，不要提交。

### `artifacts/`

本地生成的打包或检查产物。例如曾经生成过完整 eval package。它是结果快照，不是 canonical
源数据；需要重新交付时应从 `docs/case-bank/cases/` 重新 pack。

### `cases/`

早期/原始复现线索和最小客户端。OLD15 回放时也会从这里取 `candidate.json` 和 client。
它不是当前正式 case-bank 的交付目录。

重要孙文件夹：

- `cases/<case_id>/`：单个原始候选。通常包含 `candidate.json`、client 文件、README 等。
- `cases/*_toy_drift/`：各语言玩具漂移样例，主要用于 adapter 和流程打底。

### `case_bank/`

轻量 Python 入口包，支持 `python -m case_bank ...` 这类命令。现在主要是命令转发层。
大部分实际实现仍在 `silent_drift_miner/`。

### `data/`

本地验证、旧流水线、oracle、工具链记录的工作区。这里有些目录是源材料，有些是生成物，
看之前先分清。

重要孙文件夹：

- `data/curated/`：旧流水线整理过的 case 描述，可用于从 curated 转 case-bank。
- `data/oracle/`：旧流水线 oracle 材料，含 public/hidden 的历史结构。
- `data/ecosystem_gates/`：生态语言/工具链 gate 记录，用来说明哪些环境可跑。
- `data/toolchains/`：工具链探测和本地环境信息。
- `data/verification/`：本地 replay/raw evidence 工作区，通常被 `.gitignore` 忽略；不要把它当交付源。

### `docs/`

文档主目录。这里既有当前规范，也有历史路线图和各语言 idea bank。看“现在该怎么交付”，优先看
`docs/case-bank/`；看项目怎么演化，再看 phase 文档。

重要孙文件夹：

- `docs/case-bank/`：当前最重要的目录，case-bank 的规范入口、ledger、indexes 和打包提示词都在这里。
- `docs/case-bank/cases/`：canonical case 包目录。103 个包按场景分类放在这里。
- `docs/case-bank/indexes/`：由 metadata 生成的索引视图，改 case metadata 后要重建。
- `docs/case-bank/assets/`：README 用到的图和静态资产，例如状态机图。
- `docs/case-bank-restructure/`：case-bank 文件夹契约、schema、tag taxonomy、最终规划。
- `docs/verification-runs/`：早期 30/50 验证运行的人工 ledger。

### `eval_package_old15_check/`

本地生成的 eval package 检查目录，用来确认 pack 后公开包结构没问题。它是生成物，不是源码，
也不应该作为 human 的阅读入口。

### `online/`

在线服务/API 漂移线索。它们有证据价值，但不是离线可复现 case-bank 正例，不计入 46 个窄口径可送包。

重要孙文件夹：

- `online/case-library/`：在线案例库。
- `online/case-library/cases/`：单个在线平台/API 漂移记录。

### `silent_drift_miner/`

项目的主要 Python 代码、测试和配置。要改工具能力、adapter、复现逻辑、case-bank writer，
基本都在这里。

重要孙文件夹：

- `silent_drift_miner/src/silent_drift_miner/`：核心源码。
- `silent_drift_miner/src/silent_drift_miner/adapters/`：各语言 adapter。
- `silent_drift_miner/src/silent_drift_miner/adapters/common/`：adapter 共享逻辑。
- `silent_drift_miner/src/silent_drift_miner/adapters/{dotnet,go,js,jvm,php,ruby}/`：各生态具体执行器。
- `silent_drift_miner/src/silent_drift_miner/commands/`：CLI 命令实现。
- `silent_drift_miner/src/silent_drift_miner/extractors/`：从来源中抽取候选信息。
- `silent_drift_miner/src/silent_drift_miner/sources/`：来源数据接口。
- `silent_drift_miner/tests/`：测试入口，case-bank 结构测试也在这里。
- `silent_drift_miner/configs/`：运行配置。
- `silent_drift_miner/data/`：包内测试/fixture 数据，不等同于根目录 `data/`。
- `silent_drift_miner/tools/`：辅助脚本。

### `tools/`

仓库级辅助工具目录。当前内容不多，适合放一次性或跨模块的维护脚本；正式 Python 包逻辑优先放
`silent_drift_miner/src/`。

## `docs/case-bank/cases/` 下面的场景目录

这些是 case-bank 的一级分类。每个分类下面才是具体 case 包。

- `commerce-order-flow/`：订单、ERP、支付、状态同步链路。
- `inventory-and-fulfillment/`：库存、履约、商品入库和审批语义。
- `observability-and-logging/`：日志、观测字段、格式化和静默失败线索。
- `parsing-and-ingestion/`：解析、导入、CSV/URL/YAML/XML/Markdown 等输入语义。
- `routing-and-identity/`：ID、地址、路由、merchant/order/resource identity。
- `runtime-semantics/`：语言或库运行时默认行为变化。
- `serialization-and-binding/`：序列化、反序列化、配置绑定、类型映射。
- `state-and-lifecycle/`：生命周期、webhook、事件顺序、状态机、缓存/追踪行为。
- `time-and-localization/`：时间、时区、本地化、日期格式。
- `validation-and-policy/`：校验规则、策略默认值、字段 required/optional 语义。

每个具体 case 包通常长这样：

```text
docs/case-bank/cases/<scenario>/<case-slug>/
  case.md
  evidence.md
  env.md
  metadata.json
  client/
  hidden/
```

- `case.md`：给被测 agent/human 的公开任务。
- `evidence.md`：为什么这是一个真实漂移线索。
- `env.md`：环境和复现条件。
- `metadata.json`：机器读的状态、语言、标签、来源、版本等。
- `client/`：最小复现客户端。
- `hidden/`：oracle 和 expected assertions；公开 eval package 会剥离。

## 不要被这些目录误导

- `.uv-cache/`、`.uv-python/`：本地环境。
- `eval_package_old15_check/`、`artifacts/`：生成结果，不是源。
- `data/verification/`：raw replay 工作区，适合查证据，不适合作为交付入口。
- `__pycache__/`、`.pytest_cache/`：缓存。
- `node_modules/`、`vendor/`、`bin/`、`obj/`、`target/`：依赖或构建产物，看到也不要提交进 case 包。

## 最常用命令

```powershell
python -m case_bank validate --cases docs/case-bank/cases/
python -m case_bank index build --out docs/case-bank/indexes/
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package/
python -m pytest silent_drift_miner/tests/test_case_bank.py -q
```

## 一句话记法

要看可交付的包，进 `docs/case-bank/cases/`。要看怎么生成和校验，进 `silent_drift_miner/`。
要看历史和解释，进 `docs/`。看到 cache、verification、eval_package，先当成本地产物。
