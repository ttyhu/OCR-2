# OCR
CTPN+Densenet+CTC   
1，Text Detection Based on CTPN  
2，Text Recognition Based on Densenet+CTC  
  
### Environmental deployment 
```python
sh setup.sh  
```
Before the CPU environment is executed：  
the part for GPU needs to be commented out and the part for CPU needs to be uncommented.    
   
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
After decompression, pictures should be placed in ./train/images directory.  
The description files should be placed in ./train directory.  

```python
cd train
python train.py
```
  
### Theory  
## Part I（CTPN):   
# CTPN：  
1.Use the first five Conv stage of VGG16 to get the feature map，with the size of W×H×C.    
2.Use 3×3 slide windows to extraction feature in above feature map，we use these features to predict based on anchors, the define of anchor is the same as faster-rcnn，which is to help us define the target areas to be selected.  
3.Put the features from the previous step into a bidirectional LSTM, output the size of W×256，put the result into a 512-dimensional full connection layer.    
4.Finally, the output obtained by classification or regression is divided into three parts.
According to the figure above, the order from top to bottom is below :
2k vertical coordinates（Coordinates of the y-axis representing the height and center of the selection box）  
2k scores（Represents the category information of K anchors, indicating whether they are characters or not.)  
k side-refinement（Represents the horizontal offset of the selection box）  
In this project, the horizontal width of anchor is 16 pixels unchanged.  
5.Using the algorithm of text construction, we merge the slender rectangle to get the text sequence box.  

# Importance:  
1.anchor:The main difference to RPN in Faster-Rcnn is the introduction of calculus thought to cut our candidate regions into stripes. The K anchors (that is, K preferred strips) are set as follows:   
the width is 16 pixels, and the height varies from 11 to 273 pixels (multiplied by 1.4 each time).    
2.RNN is used to record the last state  
LSTM is used to record information before long and short memory  
BLSTM（two-way LSTM） is used to record information of State information before and after.      
3.Anchor combination of text boxes is mainly in the form of pairs.  
        
            
## Part II（Densenet）：  
In this project, 5990 Chinese characters are used to classify the input images. There are 5990 categories.    
The dataset is based on the above Baidu cloud links, and you can customize the data sample content you need.  
Reference：https://github.com/DongfeiJi/OCRDataGenerator  
     
### In practical application, I encounter several issues:  
Issue 1：We should pay attention to the correspondence between input coding and Chinese character subscripts.
Issue 2：The evaluation  may be different in different actual production environments.   
The training code is based on Keras and can be written by yourself.  
