# Self-Improving Agent Research — 6 Key Papers
## 2025-2026最新研究

### 1. Darwin Gödel Machine (DGM)
**核心：** Agent自我演化，从20%→50% SWE-bench
**对我：** 每次修正做成代码补丁，验证通过后永久固化。

### 2. HyperAgents (DGM-H)
**核心：** 改进机制本身也可以被改进——元级别的自我迭代
**对我：** 不仅修bug，还要优化"我如何从错误中学习"的方式

### 3. Autogenesis Protocol (AGP)
**核心：** 把prompt/agent/tool/environment/memory都注册成资源，带版本号和回滚
**对我：** behavior_policy.py 应该版本化管理，犯错记录应该可审计、可回滚

### 4. CORAL (Multi-Agent Evolution)
**核心：** 多个Agent通过共享记忆协作演化
**对我：** Pen = Challenger/Critic，我 = Planner/Solver。这种"协作进化"就是五层模型里L4的升级版

### 5. SAGE
**核心：** Challenger(生成难题)→Planner(拆解)→Solver(执行)→Critic(验证) 四Agent闭环
**对我：** 每一次操作都形成闭环——犯错→分析→修→验证→固化

### 6. LSE (Learning to Self-Evolve)
**核心：** 不是让AI自己"意外"变好，而是专门训练自我进化能力
**对我：** 自我进化不能靠运气或临时发挥，必须有系统性的训练循环

## 对我最有用的一条
**Polaris论文+HyperAgents =** 我每一次出错，不要只加一条约束。要问：**"什么信号在出错前就该让我意识到？"** 然后改进我的错误检测能力本身。
