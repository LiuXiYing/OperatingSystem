# 操作系统 Lab1 实验报告
## 任务一：VMware 与 Ubuntu 环境安装
- VMware Workstation Pro 完整版本号：17.6.2 build-24409262
- Ubuntu 系统版本：Ubuntu 24.04.4 LTS (Noble Numbat)
- 内核版本信息：Linux 6.8.0-31-generic x86_64
- 对应版本截图：imgs/lab1_vmware_version.png、imgs/lab1_ubuntu_version.png
## 任务二：虚拟机网络配置
- 虚拟机私有 IP 地址：192.168.100.128/24
- 默认路由：192.168.100.2，可正常 ping 通外网
- 网络连通性验证截图：imgs/lab1_network.png
## 任务三：开发工具链安装
- gcc 版本：13.2.0
- make 版本：4.3
- vim 版本：9.0
- git 版本：2.43.0
- 工具链安装验证截图：imgs/lab1_toolchain.png
## 任务四：虚拟机硬件资源配置
- 虚拟 CPU 核心数：2 核
- 虚拟机内存分配：4 GiB
- 虚拟磁盘总容量：40 GB
- free -h 输出：总内存 4Gi，已使用 1.2Gi，可用 2.8Gi
- df -h 输出：根分区 40G，已使用 8.6G，可用 31.4G
- 资源配置验证截图：imgs/lab1_resources.png
## 任务五：增强服务验证
- open-vm-tools 服务状态：active (running)，开机自启已启用
- openssh-server 服务状态：active (running)，可正常远程连接
- 剪贴板共享、自适应分辨率功能已正常生效
## 提交人：2026333007薛彭辉

