# ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents

<p align="center">
   <a href="https://arxiv.org/abs/2508.14040" target="_blank">📃 Paper </a>
   &nbsp;|&nbsp;
   <a href="https://docs.google.com/spreadsheets/d/1wFHvf3mb42j74JtAww4CTOc7tdF8KIfGZyRQyLhh5pc/edit?usp=sharing" target="_blank">📊 OfficeWorld Leaderboard</a>
</p>

_Read this in [English](README.md)._

本仓库是 ComputerRL 的代码仓库，基于对 OSWorld 仓库的修改与简化。ComputerRL 专注于用于训练计算机使用智能体的端到端在线强化学习方法。该项目在 OSWorld 基准环境的基础上进行了优化与简化，为计算机使用研究提供了更聚焦、更高效的实验平台。

<p align="center">
    <img src="assets/framework.png" alt="框架概览" width="100%"><br>
    <em>我们提出了一种 API-GUI 行动范式，将自动构建的 API 与 GUI 操作无缝融合，以提升智能体的效率与效果。以及一个包含 1,000+ 真实场景实例的大规模并行桌面环境，结合异步强化学习框架，实现高效采样与稳健的智能体训练。</em>
</p>

<p align="center">
    <img src="assets/results.png" alt="Main Results" width="60%"><br>
    <em>OSWorld 上主流智能体的成功率。</em>
</p>

## 🌱 环境

### 🖥️ 检查 KVM 支持

我们建议在启用 KVM 支持的情况下运行虚拟机，以获得更好的性能。要检查系统是否支持 KVM，运行以下命令：
```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```
如果输出结果大于 0，则表示系统支持 KVM。 ✅

### 🐳 安装 Docker

请参考 [Docker 安装指南](https://docs.docker.com/desktop/setup/install) 在你的机器上安装 Docker。

### 📥 下载镜像

从 [ubuntu_osworld](https://huggingface.co/datasets/xlangai/ubuntu_osworld) 下载官方镜像。

---

## 🧪 实验

### 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 📂 下载实验文件

所有实验文件会缓存到 `./cache`目录下。可以通过以下方法获取实验文件：

- **OSWorld:** 你可以参考 [OSWorld 官方仓库](https://github.com/xlang-ai/OSWorld) 下载所有缓存文件。
- **OfficeWorld:** 从 [ModelScope/OfficeWorld-Cache](https://www.modelscope.cn/datasets/shawliu9/OfficeWorld) 下载实验文件，并解压到 `./cache` 目录。

### 🤖 部署模型

我们开源了两种类型的模型。你可以下载这些模型，并通过设置`--model`参数指定模型名称：
- **Text-Only:** [ModelScope/ComputerRL](https://www.modelscope.cn/models/shawliu9/computerrl-glm4-9b)
- **Multimodal:** [ModelScope/ComputerRL-V](https://www.modelscope.cn/models/shawliu9/computerrl-glm4_1v-9b)

```bash
pip install "sglang[all]"  # if not installed

python -m sglang.launch_server \
  --model zai-org/autoglm-os-9b \
  --host 0.0.0.0 --port 30000 --served-model-name autoglm-os
```

### 🚀 运行实验

运行以下脚本以在 OSWorld 上复现实验结果。

#### 🔐 环境变量
```bash
# Set up your API
export OPENAI_BASE_URL="https://api-gateway.glm.ai/v1"
export OPENAI_API_KEY="API-KEY"
```

#### 🔄 单进程测试

```bash
# If using a multimodal model, please use run_autoglm_v.py
python run_autoglm.py \
    --provider_name docker \
    --path_to_vm Ubuntu/Ubuntu.vmx \
    --headless \
    --max_steps 15 \
    --test_all_meta_path ./evaluation_examples/test_nogdrive.json
```

#### ⚡ 并行测试

```bash
# If using a multimodal model, please use run_multienv_autoglm_v.py
python run_multienv_autoglm.py \ 
    --provider_name docker \
    --path_to_vm Ubuntu/Ubuntu.vmx \
    --headless \
    --num_workers 20 \
    --max_steps 15 \
    --test_all_meta_path ./evaluation_examples/test_nogdrive.json
```

### 📊 查看实验结果

结果文件会缓存到 `./results`。运行以下脚本查看分数：

```bash
python show_result.py
```

### 🧹 清理 Docker 镜像

完成实验后，可能会遗留一些 Docker 镜像。使用以下命令进行清理：

```bash
docker stop $(docker ps -q) && docker rm $(docker ps -a -q)
```

---

## 🏢 OfficeWorld 基准

OfficeWorld 基准构建自 [SpreadsheetBench](https://github.com/RUCKBReasoning/SpreadsheetBench)、[PPTC](https://github.com/gydpku/PPTC) 以及自研的 Writer 领域任务。  
任务经过必要的适配以融入 OSWorld 框架，使得能够对面向办公场景的智能体能力进行系统化评估。

### ▶️ 运行 OfficeWorld 基准

运行以下命令，在 OfficeWorld 基准上评估你的智能体：

```bash
python run_multienv_autoglm.py \
    --provider_name docker \
    --path_to_vm Ubuntu/Ubuntu.vmx \
    --headless \
    --num_workers 20 \
    --max_steps 15 \
    --test_all_meta_path ./evaluation_examples/test_office.json
```

### 🏆 排行榜

在此查看排行榜 [here](https://docs.google.com/spreadsheets/d/1wFHvf3mb42j74JtAww4CTOc7tdF8KIfGZyRQyLhh5pc/edit?usp=sharing)! 🚀

如果你希望将结果添加到排行榜，请发送邮件至 [`hanyullai@outlook.com`](mailto:hanyullai@outlook.com)。

## 📄 引用

```
@misc{lai2025computerrl,
    title={ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents}, 
    author={Hanyu Lai and Xiao Liu and Yanxiao Zhao and Han Xu and Hanchen Zhang and Bohao Jing and Yanyu Ren and Shuntian Yao and Yuxiao Dong and Jie Tang},
    year={2025},
    eprint={2508.14040},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2508.14040}, 
}
```