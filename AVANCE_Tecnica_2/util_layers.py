
from __future__ import absolute_import

import tensorflow as tf
from tensorflow.keras.layers import Layer

def drop_path_(inputs, drop_prob, is_training):
    
    # Bypass in non-training mode
    if (not is_training) or (drop_prob == 0.):
        return inputs

    # Compute keep_prob
    keep_prob = 1.0 - drop_prob

    # Compute drop_connect tensor
    input_shape = tf.shape(inputs)
    batch_num = input_shape[0]
    rank = tf.rank(inputs)

    #shape = (batch_num,) + (1,) * (rank - 1)
    shape = tf.concat([[batch_num], tf.ones(rank - 1, dtype=tf.int32)], axis=0)
    random_tensor = keep_prob + tf.random.uniform(shape, dtype=inputs.dtype)
    path_mask = tf.floor(random_tensor)
    output = tf.math.divide(inputs, keep_prob) * path_mask
    return output

class drop_path(Layer):
    def __init__(self, drop_prob=None,**kwargs):
        super().__init__()
        self.drop_prob = drop_prob

    def get_config(self):

        config = super().get_config().copy()
        config.update({
            'drop_prob': self.drop_prob
        })
        return config


    def call(self, x, training=None):
        return drop_path_(x, self.drop_prob, training)