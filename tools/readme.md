# tools文件夹内程序使用说明



## 确定颜色的 HSV 阈值

### 阈值编辑器 `threshold_editor.py`

在连接机器人后运行程序，通过拖动滚动条让画面中的只留下想要的颜色部分。

记录下各个部分相对应的值。

**注意：**滚动条的 min 值不可以大于 max 值





## 机器学习

### 数据采集器 `data_collector.py`

每一次拍摄的文件路径会保存在当前目录下

文件夹名由程序内 CLASSES_DIR 所定义



### 训练模型 `model_trainer.py`

首次运行会下载相关文件。

确认文件内 SAMPLE_DIR 和 data_collector.py内 CLASSES_DIR 类似



### KNN分类器  `knn_classifier.py`

连接机器人后运行程序