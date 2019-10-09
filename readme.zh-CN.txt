用于 VMware Workstation 的 macOS Unlocker V3.0
==============================================

+-----------------------------------------------------------------------------+
| 重要提醒：                                                                    |
| =========                                                                   |
|                                                                             |
| 请在使用新版本 Unlocker 前卸载旧版本,否则 VMWare 可能会无法使用。                  |
|                                                                             |
|                                                                             |
+-----------------------------------------------------------------------------+

1. 介绍
-------

Unlocker 3 适用于 VMware Workstation 11-15 以及 Player 7-15。

如果您正使用早期版本的 VMWare，请继续使用 Unlocker 1。

Unlocker 3 已对以下情况进行了测试：

* 在 Windows 或 Linux 上的 Workstation 11/12/14/15
* 在 Windows 或 Linux 上的 Workstation Player 7/12/14/15

根据所修补的产品，本代码会作出以下修改：

* 修补 vmware-vmx 及其相关组件，以允许 Mac OS 启动。
* 修补 vmwarebase .dll 或 .so，以允许创建虚拟机过程中选择 Apple 作为客户机操作系统。
* 下载一份最新的用于 Mac OS 的 VMWare Tools 副本。

请注意，并非所有的 VMWare 版本都能通过“安装 VMWare Tools”菜单项识别 darwin.iso。
例如，在 Workstation 11、Player 7上，您需要手动挂载 darwin.iso。

无论何时都请确保 VMware 未在运行且所有后台的客户机都已关闭。

本软件的代码是用 Python 编写的。

2. 先决条件
-----------

本代码需要 Python 2.7 以正常工作。大多数 Linux 发行版都附带一个兼容的 Python 解释器，
因此本代码应可在不需要任何额外软件的情况下工作。

Windows 版本的 Unlocker 有一个使用 PyInstaller 的打包版 Python 脚本，因此无需在计算机
上安装 Python。

3. 限制
-------

如果您使用的是用于 Windows 的 VMware Player 或 Workstation，您可能会得到一个核心转储文件。

最新的 Linux 版本 VMWare 则不会出现此问题。

+-----------------------------------------------------------------------------+
| 重要提醒：                                                                   |
| =========                                                                   |
|                                                                             |
| 如果您创建一个新的虚拟机，VMware 可能会停止工作并创建一个核心转储文件。              |
| 有两种方法可以解决这个问题：                                                    |
|                                                                             |
| 1. 将虚拟机的硬件兼容性设置为 Workstation 10 - 这不会影响性能。                   |
| 2. 编辑 VMX 文件并添加：                                                      |
|    smc.version = "0"                                                        |
|                                                                             |
+-----------------------------------------------------------------------------+

4. Windows
----------
在 Windows 下，您可以通过以管理员身份运行 cmd.exe 再在其中运行脚本，或在资源管理
器里右击脚本并选择“以管理员身份运行”。

win-install.cmd   - 修补 VMware
win-uninstall.cmd - 还原 VMware
win-update-tools.cmd - 检索最新的用于 Mac OS 的 VMWare Tools

5. Linux
--------
在 Linux 下，您需要是 root 用户，或使用 sudo 运行脚本。

您可能需要通过对下面三个脚本中的前两个运行 chmod +x 来确保它们具有执行权限。

lnx-install.sh   - 修补 VMware
lnx-uninstall.sh - 还原 VMware
lnx-update-tools.sh - 检索最新的用于 Mac OS 的 VMWare Tools
   
6. 致谢
-------

感谢 Zenith432 最初构建了 C++ 版本的 Unlocker，还要感谢 Mac Son of Knife（MSoK）
的所有测试与支持。

同样感谢 Sam B 找到了针对 ESXi 6 的解决方案，并帮我进行了专业的调试。Sam 还编写了
修补 ESXi ELF 文件的代码，并编辑了 Unlocker 的代码使其能在 ESXi 6.5 的环境下运行
在 Python 3 上。


更新历史
--------
2018/09/27 3.0.0 - 首个发行版
2018/10/02 3.0.1 - 修正了 gettools.py 使其能在 Python 3 环境下正常工作且能正确下
                   载 darwinPre15.iso
2018/10/10 3.0.2 - 修正了带有 Windows 可执行程序的杀毒软件对本程序的误报
                 - 允许 Python 2 和 3 从 Bash 脚本运行 Python 代码

(c) 2011-2018 Dave Parsons
