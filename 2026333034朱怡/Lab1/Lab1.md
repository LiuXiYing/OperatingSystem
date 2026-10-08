# Lab1 实验步骤
## 一、VMware Workstation安装
1. 打开VMware安装包，同意许可协议
2. 按需取消两个可选组件勾选，点击下一步
3. 完成安装，启动VMware，关闭自动更新弹窗
📷截图：VMware安装完成界面！
![VMware安装完成界面](https://github.com/zy1111468/OperatingSystem/blob/main/2026333034%E6%9C%B1%E6%80%A1/Lab1/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE2026-10-07%20225504.png?raw=true)
## 二、新建Ubuntu虚拟机
1. VMware主页点击【创建新的虚拟机】，典型安装
2. 选择ISO镜像文件，选中Ubuntu镜像
3. 设置虚拟机名称与存储位置
4. 内存分配2GB，处理器默认1核
5. 创建虚拟磁盘，20GB，单个文件存储
6. 核对硬件配置，完成并启动虚拟机
📷截图：虚拟机硬件配置概览页
![虚拟机硬件配置概览页](https://github.com/zy1111468/OperatingSystem/blob/main/2026333034%E6%9C%B1%E6%80%A1/Lab1/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-10-07%20225244.png?raw=true)
## 三、Ubuntu系统安装
1. 启动虚拟机，语言选择简体中文
2. 选择【安装Ubuntu】，不选试用
3. 勾选下载更新、第三方软件
4. 磁盘：擦除磁盘并安装（仅虚拟机磁盘）
5. 时区默认上海
6. 设置用户名、计算机名、登录密码
7. 等待安装，结束后点击现在重启
📷截图：安装类型页面、账号创建页面
![安装类型页面、账号创建页面](https://github.com/zy1111468/OperatingSystem/blob/main/2026333034%E6%9C%B1%E6%80%A1/Lab1/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-10-07%20225504.png?raw=true）(https://github.com/zy1111468/OperatingSystem/blob/main/2026333034%E6%9C%B1%E6%80%A1/Lab1/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-10-07%20225722.png?raw=true))
## 四、Ubuntu开机初始化
1. 重启后输入密码登录桌面
2. 数据收集弹窗：选择不发送
3. 关闭欢迎向导，进入桌面
📷截图：Ubuntu桌面首页
![：Ubuntu桌面首页](https://github.com/zy1111468/OperatingSystem/blob/main/2026333034%E6%9C%B1%E6%80%A1/Lab1/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-10-08%20114033.png?raw=true)
## 五、安装open-vm-tools（复制粘贴功能）
1. 打开终端 `Ctrl+Alt+T`
2. 更新源
```bash
sudo apt update
