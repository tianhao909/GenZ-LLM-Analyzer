# GenZ
Generative LLM Analyzer

- [GenZ](#genz)
  - [Overview](#overview)
    - [Installation](#installation)
  - [Examples](#examples)
  - [Parallelism Scheme](#parallelism-scheme)
  - [Communication](#communication)
  - [Data Types](#data-types)
  - [TODOs](#todos)
  - [Citation](#citation)

## Overview

GenZ to designed to simply the relationship between the hardware platform used for serving Large Language Models(LLMs) and inference serving metrics like latency and memory.

Running an LLM on hardware has three key component.
- Model : The LLM model architecture and corresponding parameters like number of layers, layer dimension etc.
- Usecase : Size of the Input queries, expected size of output query, and number of parallel beams generated.
- Optimization : There are various different optimizations that can be used to improve the LLM performance on a given hardware platform.
  - Quantization (Reducing the data precision)
  - Batching (Batching multiple similar sized queries to improve the throughput)
  - Parallelization ( Choosing specific parallelization strategies can help improve the performance of the LLM).
  - Operator Fusion ( FlashAttention/FLAT are techniques used to fuse multiple kernels together to speedup certain kernels.)
GenZ旨在简化用于服务大型语言模型（LLMs）和推理服务指标（如延迟和内存）的硬件平台之间的关系。

在硬件上运行LLM有三个关键组成部分：

模型：LLM模型架构及其相关参数，如层数、层维度等。
使用案例：输入查询的大小、预期输出查询的大小以及生成的并行beam数量。
优化：有多种不同的优化方法可用于提高给定硬件平台上LLM的性能。
量化（减少数据精度）
批处理（将多个大小相似的查询进行批处理，以提高吞吐量）
并行化（选择特定的并行化策略可以帮助提高LLM的性能）
操作融合（FlashAttention/FLAT是将多个核心融合在一起以加速某些核心的技术）


Given the specified LLM, Hardware Platform(GPU/CPU/Accelerator), data type, and parallelism configurations, genz can generate the latency and memory usage estimations.

GenZ can help answer various system-level choice-making questions, including,  
- how should the deployment platform change for LLM use cases for Q/A chatbots for customer services agents versus legal document summarization in attorney's offices? 
- how can the platform configurations be tweaked to maintain the same level of performance when deploying LLaMA2-70B instead of LLaMA2-7B?
- What will be the performance compromise if we do not change the serving platform?

GenZ can help computer architects understand trends which can help in designing the next generation of AI platforms by navigating the interplay between various HW characteristics and LLM inference performance based on models and compute demand. 
- if each node's total HBM bandwidth increases/decreases by 10\%, what would the impact on inference latency be? 
- By how much should the chip-to-chip communication network be improved? 
  
根据指定的LLM、硬件平台（GPU/CPU/加速器）、数据类型和并行配置，GenZ可以生成延迟和内存使用的估计。

GenZ可以帮助回答各种系统级选择问题，包括：

在为客户服务代理的Q/A聊天机器人与律师事务所的法律文件摘要化的LLM使用案例中，部署平台应该如何变化？
当部署LLaMA2-70B而不是LLaMA2-7B时，如何调整平台配置以保持相同的性能水平？
如果不更改服务平台，性能会有什么妥协？
GenZ可以帮助计算机架构师了解趋势，从而在基于模型和计算需求的基础上设计下一代AI平台，通过导航各种硬件特性与LLM推理性能之间的相互作用。

如果每个节点的总HBM带宽增加/减少10%，对推理延迟会有什么影响？
需要将芯片间通信网络改进多少才能达到什么性能水平？


### Installation

```sh
git clone abhibambhaniya/genz.git
cd genz
pip install -r requirements.txt
```

## Examples

Refere to notebook/LLM_inference_perf.ipynb and notebook/LLM_memory_analysis.ipynb to get familiar with the setup.
请参考 notebook/LLM_inference_perf.ipynb 和 notebook/LLM_memory_analysis.ipynb 以熟悉设置。



## Parallelism Scheme
GenZ supports Tensor Parallelism (TP), Pipeline Parallelism (PP) accross large platforms with multiple NPUs.
并行方案
GenZ支持跨多个NPU的张量并行（TP）和流水线并行（PP）。


## Communication
Tensor Parallelism requires `ring allreduce`. Pipeline Parallelism requires a single hop node-to-node message passing.
通信
张量并行需要 ring allreduce。流水线并行需要单跳节点间的消息传递。


## Data Types
Data types are expressed with the number of bits, We have the following data types are modeled for now.
数据类型
数据类型用位数表示，目前我们模型支持以下数据类型：


| Data Type | Bits |
|:---------:|:----:|
|    FP32   |  32  |
|    BF16   |  16  |
|  INT8/FP8 |   8  |
|  INT4/FP4 |   4  |
|    INT2   |   2  |

## TODOs
Check the TODOs below for what's next and stay tuned! Any contributions or feedback are highly welcome!

- [ ] Add Expert parallelism and Sequence parallelism
- [ ] Support LoRA
- [ ] Add different kind of quantization for weights/KV/activations.
待办事项
查看下面的待办事项，了解接下来的计划，敬请关注！欢迎任何贡献或反馈！

 添加专家并行性和序列并行性
 支持 LoRA
 添加不同类型的权重/KV/激活的量化方法



## Citation

If you use GenZ in your work, please cite:
引用
如果您在工作中使用了GenZ，请引用：

```

```

