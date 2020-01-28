## 思路
opencv读取视频后，通过SVM进行车辆检测，检测疑似为车牌后。使用HyperLPR进行二次识别，得出准确结果

## 关键点
本文使用SVM进行车牌检测；
使用HyperLPR进行车牌识别；
视频部分，使用2个进程进行，解决实时读取延迟问题

## 致谢
rtsp视频流读取 https://github.com/Yonv1943/Python.git https://zhuanlan.zhihu.com/p/38136322
车牌识别 https://github.com/zeusees/HyperLPR.git
车牌haar模型 https://github.com/kraten/vehicle-speed-check.git