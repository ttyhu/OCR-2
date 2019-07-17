# OCR
CTPN+Densenet+CTC   
1，Text Detection Based on CTPN  
2，Text Recognition Based on Densenet+CTC  
  
### Environmental deployment 
```python
sh setup.sh  
```
Before the CPU environment is executed, the part for GPU needs to be commented out and the part for CPU needs to be uncommented.    
   
### Inference     
Put the test images in the ./test_images, and the test results will be saved in ./test_results.  
```python
python test.py   
```
  
### Train  
1.Train CTPN，See for details in ./ctpn/README.md     
2.Train Densenet   
Dataset：https://pan.baidu.com/s/1QkI7kjah8SPHwOQ40rS1Pw (Password：lu7m)  
A total of 3.64 million pictures were divided into 99:1 images with a resolution of 280x32.  
After decompression, pictures should be placed in ./train/images directory and the description files should be placed in ./train directory.  

```python
cd train
python train.py
```
  
### Theory  
Part I（CTPN):   
CTPN：  
1.use the first five Conv stage of VGG16 to get the feature map，with the size of W×H×C.    
2.use 3×3 slide windows to extraction feature in above feature map，we use these features to predict based on anchors, the define of anchor is the same as faster-rcnn，which is to help us define the target areas to be selected.  
3.将上一步得到的特征输入到一个双向的 LSTM中，输出 W×256的结果，再将这个结果输入到一个512维的全连接层。  
4.最后通过分类或回归得到的输出主要分为三部分，根据上图从上到下依次为2k vertical coordinates（表示选择框的高度和中心的y轴的坐标）；2k scores（表示的是k个 anchor的类别信息，说明其是否为字符）；k side-refinement（表示的是选择框的水平偏移量）。本文实验中anchor的水平宽度都是16个像素不变。  
5.用文本构造的算法，将我们得到的细长的矩形合并成文本的序列框。  
重点:  
1.anchor:和 Faster-Rcnn中的RPN的主要区别在于引入了微分思想，将我们的的候选区域切成长条形的框来进行处理。k个 anchor（也就是k个待选的长条预选区域）的设置如下：宽度都是16像素，高度从11~273像素变化（每次乘以1.4）。  
2.RNN用于记录上一时刻状态，LSTM长短记忆之前的状态信息，BLSTM（双向LSTM）可以长短记忆之前和之后的状态信息。   
3.anchor文本框的合并，主要是采用pairs的形式。  
        
            
第二部分（Densenet）：  
这里文字识别实现方式，其实就是分类，本项目采用了5990个汉字，对输入图像进行分类，共有5990类别。  
数据集是基于上述百度云链接，同时你也可以自定义生成自己所需要的数据样本内容。  
参考链接：https://github.com/DongfeiJi/OCRDataGenerator  
     
实际应用我遇到几个坑：  
坑1:输入编码与汉字下标对应问题，大家可以注意一下。  
坑2:指标问题，面对不同实际生产环境，采用的评价指标可能不同，训练代码是基于Keras进行编写，可以自行编写指标代码。
