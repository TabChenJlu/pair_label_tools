# pair_label_tools

可以用来标注pair形式的数据

## 使用步骤

### 初始化系统
1、将需要比较的文件保存到data/raw_data 下，或者修改配置文件config/system.ini 中的 `data_dir`

2、执行`python3 init.py`，将代标注的数据写入到数据库

3、`python3 start.py`，开启服务

### 开始标注
1、点击**开始**，开始标注，如下图
![](https://ws4.sinaimg.cn/large/006tKfTcly1g102grw79qj325y0i0404.jpg)

2、左边好就点**左边**，右边好就点**右边**，点击完会自动加载下一个不需要重新点开始。
![](https://ws1.sinaimg.cn/large/006tKfTcly1g102j6vfnwj325s0q8114.jpg)

注意：开始点击一次就可以
