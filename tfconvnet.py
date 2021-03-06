import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data

# Convolucao: 1x1 com stride (passo) 1
def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1],
                            padding='SAME')


# Max pooling: 2x2 com stride 2
def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], 
                           strides=[1, 2, 2, 1],
                           padding='SAME')

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)


def bias_variable(shape):
	initial = tf.constant(0.5, shape=shape)
	return tf.Variable(initial)

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
sess = tf.InteractiveSession()

# Primeira camada convolucional
x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1, 28, 28, 1])

W_conv1 = weight_variable([5, 5, 1, 96])
b_conv1 = bias_variable([96])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# Segunda camada convolucional
W_conv2 = weight_variable([3, 3, 96, 256])
b_conv2 = bias_variable([256])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# Camada densamente conectada
W_fc1 = weight_variable([7 * 7 * 256, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 256])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)


# Dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


# Camada de saida
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# Funcao de custo
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv),
                                reduction_indices=[1]))


# Otimizador: Adam (Adaptive Moment Estimation)
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# Inicializar variaveis
sess.run(tf.initialize_all_variables())


correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))


# Precisao
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

plt.axis([0, 20000, 0, 1])
plt.ion()

for i in range(200000):
  batch_xs, batch_ys = mnist.train.next_batch(50)
  if i % 100 == 0:
    train_accuracy = accuracy.eval(feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 0.5})
    print("[Treinamento] Passo %d, precisao: %g" % (i, train_accuracy))
    plt.scatter(i, train_accuracy)
    plt.pause(0.1)
    plt.show()


  train_step.run(feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 0.5})


print("[Teste] precisao: %g" % accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 0.5}))


