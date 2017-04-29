import os
import scipy.misc
import numpy as np

from model import DCGAN
from utils import pp, visualize, to_json, show_all_variables

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_integer("epoch", 25, "Epoch to train [25]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_integer("batch_size", 64, "The size of batch images [64]")
flags.DEFINE_integer("test_num", 100, "The size of test characters [100]")
flags.DEFINE_integer("c_dim", 1, "Dimension of image color. [1]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
flags.DEFINE_boolean("is_train", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")
flags.DEFINE_string("source_font", None, "The source font npy file")
flags.DEFINE_integer("source_height", 32, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("source_width", 32, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_string("target_font", None, "The target font npy file")
flags.DEFINE_integer("target_height", 32, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("target_width", 32, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("tv_penalty", 0.0002, "Total variation penalty. [0.0002]")
flags.DEFINE_integer("L1_penalty", 50, "L1 penalty between source and the output of G. [50]")

FLAGS = flags.FLAGS

def main(_):
  pp.pprint(flags.FLAGS.__flags)

  if not os.path.exists(FLAGS.checkpoint_dir):
    os.makedirs(FLAGS.checkpoint_dir)
  if not os.path.exists(FLAGS.sample_dir):
    os.makedirs(FLAGS.sample_dir)

  #gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
  run_config = tf.ConfigProto()
  run_config.gpu_options.allow_growth=True

  with tf.Session(config=run_config) as sess:
    dcgan = DCGAN(
        sess,
        batch_size=FLAGS.batch_size,
        test_num=FLAGS.test_num,
        c_dim=FLAGS.c_dim,
        checkpoint_dir=FLAGS.checkpoint_dir,
        sample_dir=FLAGS.sample_dir,
        source_font=FLAGS.source_font,
        source_height=FLAGS.source_height,
        source_width=FLAGS.source_width,
        target_font=FLAGS.target_font,
        target_height=FLAGS.target_height,
        target_width=FLAGS.target_width,
        tv_penalty = FLAGS.tv_penalty,
        L1_penalty = FLAGS.L1_penalty)

    show_all_variables()
    if FLAGS.is_train:
      dcgan.train(FLAGS)
    else:
      if not dcgan.load(FLAGS.checkpoint_dir):
        raise Exception("[!] Train a model first, then run test mode")
      

    # to_json("./web/js/layers.js", [dcgan.h0_w, dcgan.h0_b, dcgan.g_bn0],
    #                 [dcgan.h1_w, dcgan.h1_b, dcgan.g_bn1],
    #                 [dcgan.h2_w, dcgan.h2_b, dcgan.g_bn2],
    #                 [dcgan.h3_w, dcgan.h3_b, dcgan.g_bn3],
    #                 [dcgan.h4_w, dcgan.h4_b, None])

    # Below is codes for visualization
    OPTION = 1
    visualize(sess, dcgan, FLAGS, OPTION)

if __name__ == '__main__':
  tf.app.run()
