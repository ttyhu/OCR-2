from tensorflow.python import pywrap_tensorflow
checkpoint_path = 'checkpoints/VGGnet_fast_rcnn_iter_50000.ckpt'
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
for key in var_to_shape_map:
    print("tensor_name: ", key)
