.. _beginnger:

####################################
GomerX SDK 新手入门
####################################


SDK 能做什么?
_____________

GomerX  SDK （以下简称 SDK）是一套面向 GomerX 系列产品的开发工具包，
目前支持的产品包括 。通过 SDK， 用户可以实现在PC上控制机器人运动以及获取机器人传感器的相关信息 

第一个SDK程序
_____________

接下来本文档将从如何获取 GomerX 机器人的相关信息来编写第一个 SDK 程序

- 首先从安装的的 `gomerx` 包中导入自己需要的模块，这里我们导入包含获取机器人信息的 `robot` 模块::

    from gomerx import robot

- 接下来先定义一个 `robot_name` 变量来存放机器人的名字，并实例化一个机器人对象::

    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)

-  通过 `robot` 模块中的 get_version 方法可以得到机器人的版本,并通过print函数打印出来::

    version = my_robot.get_version()
    print("Robot Version: ", version)

-  通过 `robot` 模块中的 get_sn 方法可以得到机器人的 sn 号,并通过print函数打印出来::

    sn = my_robot.get_sn()
    print("Robot SN: ", sn)

-  通过 `robot` 模块中的 get_battery 方法可以得到机器人的剩余电量,并通过print函数打印出来::

    battery = my_robot.get_battery()
    print("Robot Battery: ", battery)

示例文档中提供了获取机器人相关信息的例程 :file:`/examples/00_basic/02_robot_info.py`

.. literalinclude:: ./../../../examples/00_basic/02_robot_info.py
   :language: python
   :linenos:
   :lines: 1-12


使用示例程序
___________________

1. 更多的示例程序路径为 ``/gomerx-sdk/examples``

2. 接下来本文档将演示如何使用 SDK 所提供的示例程序

-  在终端面板输入, 将我们的终端切换到有示例程序的路径下::

    cd .\examples\00_basic\ 

-  使用 python 运行示例程序::

    python .\01_sdk_version.py

.. image:: ./../images/win10_use_SDK_examples_setup1.png

