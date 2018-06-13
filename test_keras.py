import tensorflow as tf
import os
import keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Input, Reshape, Flatten, Activation
from keras.initializers import TruncatedNormal, Constant
from keras.models import Model
import keras.backend as K

LOGDIR = './data/mnist_tutorial_keras/'
SPRITES = os.path.join(os.getcwd(), 'sprite_1024.png')
LABELS = os.path.join(os.getcwd(), 'labels_1024.tsv')

mnist = tf.contrib.learn.datasets.mnist.read_data_sets(train_dir=LOGDIR + "data", one_hot=True)


def mnist_model(learning_rate, two_conv_layer, two_fc_layer, writer):
    
    with K.name_scope('input'):
        x = Input(shape=(784,))
        x_image = Reshape((28, 28, 1))(x)

    with K.name_scope('Conv'):
        conv1 = Conv2D(16, kernel_size=(5, 5))(x_image)
        conv_out = MaxPooling2D(pool_size=(2, 2))(conv1)

    with K.name_scope('Dense'):
        flattened = Flatten()(conv_out)
        fc1 = Dense(10)(flattened)

    with K.name_scope('logits'):
        logits = Activation('softmax')(fc1)
    
    model = Model(inputs=x, outputs=logits)
    model.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    sess = K.get_session()    
    writer.add_graph(sess.graph)

    for i in range(100):
        batch = mnist.train.next_batch(100)

        results = model.train_on_batch(batch[0], batch[1])
        
        if i % 5 == 0:
            print(results)
            
    
    K.clear_session()

def make_hparam_string(learning_rate, two_conv_layer, two_fc_layer):
    return 'l={}-fc={}-conv={}'.format(learning_rate, two_fc_layer, two_conv_layer)

def main():
    for learning_rate in [1E-3, 1E-4, 1E-5]:
        for two_conv_layer in [True, False]:
            for two_fc_layer in [True, False]:
                hparam_str = make_hparam_string(learning_rate, two_conv_layer, two_fc_layer)
                print(hparam_str)
                writer = tf.summary.FileWriter('./logs/mnist_keras/' + hparam_str)

                mnist_model(learning_rate, two_conv_layer, two_fc_layer, writer)

if __name__ == '__main__':
    main()