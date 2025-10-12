# ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents

This repository is the code repository for ComputerRL, which is based on modifications and simplifications of the OSWorld repository. ComputerRL focuses on end-to-end online reinforcement learning methods for training computer use agents. This project has been optimized and simplified based on the OSWorld benchmark environment, providing a more focused and efficient experimental platform for computer use research.

<p align="center">
    <img src="assets/framework.png" alt="Framework Overview" width="100%"><br>
    <em>We introduce an API-GUI action paradigm that seamlessly integrates automatically constructed APIs with GUI actions to improve agent efficiency and effectiveness. A large-scale parallel desktop environment with 1,000+ real-world instances, combined with an asynchronous RL framework, enables efficient sampling and robust agent training.</em>
</p>

<p align="center">
    <img src="assets/results.png" alt="Main Results" width="60%"><br>
    <em>The success rates of agents on OSWorld.</em>
</p>

## 💾 Installation
### Docker (Server with KVM Support for Better Performance)
If you are running on a server, we recommend using Docker support.

#### Prerequisite: Check if your machine supports KVM
We recommend running the VM with KVM support. To check if your hosting platform supports KVM, run
```
egrep -c '(vmx|svm)' /proc/cpuinfo
```
On Linux. If the return value is greater than zero, the processor should be able to support KVM.
> **Note**: macOS hosts generally do not support KVM. You are advised to use VMware if you would like to run OSWorld on macOS.

#### Install Docker
If your hosting platform supports a graphical user interface (GUI), you may refer to [Install Docker Desktop on Linux](https://docs.docker.com/desktop/install/linux/) or [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/) based on your OS. Otherwise, you may [Install Docker Engine](https://docs.docker.com/engine/install/).

#### Running Experiments
Add the following arguments when initializing `DesktopEnv`: 
- `provider_name`: `docker`
- `os_type`: `Ubuntu` or `Windows`, depending on the OS of the VM
> **Note**: If the experiment is interrupted abnormally (e.g., due to interrupt signals), residual Docker containers may remain, which can potentially affect system performance over time. Please run `docker stop $(docker ps -q) && docker rm $(docker ps -a -q)` to clean up.

### AWS
Using cloud services for parallel evaluation can significantly accelerate evaluation efficiency (can reduce evaluation time to within 1 hour through parallelization). 
We provide comprehensive AWS support with a Host-Client architecture that enables large-scale parallel evaluation of OSWorld tasks. 

## 🧪 Experiments
### Running AutoGLM-OS

> **⚠️ Important Configuration Requirements:**
> * **Proxy Configuration**: Some tasks may require proxy settings to function properly (this depends on the strength of website defenses against your network location). Please refer to the system's proxy configuration documentation for details.
> * **Cache Configuration**: In the task init stage, the task cache will be automatically downloaded, but proxy configuration is required. You can refer to the OSWorld repository to download all caches for convenience.
> * **Impact of Missing Configuration**: If these configurations are not properly set up, the corresponding tasks will fail to execute correctly, resulting in lower evaluation scores.


To run the AutoGLM-OS agent in our paper, you can execute the following command:

Set the **OPENAI_API_KEY** environment variable with your API key
```bash
export OPENAI_API_KEY='your_openai_api_key'
```

Optionally, set **OPENAI_BASE_URL** to use a custom OpenAI-compatible API endpoint
```bash
export OPENAI_BASE_URL='http://your-custom-endpoint.com/v1'  # Optional: defaults to https://api.openai.com
```

Single-threaded execution
```bash
python run_autoglm.py \
    --provider_name docker \
    --path_to_vm Ubuntu/Ubuntu.vmx \
    --headless \
    --num_workers 20 \
    --max_steps 15 \
    --test_all_meta_path ./evaluation_examples/test_nogdrive.json
```

Parallel execution (example showing switching provider to `docker`)
```bash
python run_multienv_autoglm.py \
    --provider_name docker \
    --path_to_vm Ubuntu/Ubuntu.vmx \
    --headless \
    --num_workers 20 \
    --max_steps 15 \
    --test_all_meta_path ./evaluation_examples/test_nogdrive.json
```

To run the multimodal agent, replace the file name with `_v` version.

The results, which include screenshots, actions, and video recordings of the agent's task completion, will be saved in the `./results` (or other `result_dir` you specified) directory in this case. 
You can then run the following command to obtain the result:
```bash
python show_result.py
```