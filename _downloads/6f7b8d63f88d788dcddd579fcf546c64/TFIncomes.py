#!/usr/bin/env python3

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

import PluginsPy

@PluginsPy.addRun
class TFIncomes:

    """
    训练ax + b = y模型

    @data(default/incomes.csv): mediapipe hand数据
    """

    def __init__(self, kwargs):

        #print('Tensorflow version: {}'.format(tf.__version__))#两个下划线

        data=pd.read_csv(kwargs["data"])#. means 当前目录下
        print(data)

        x=data.Education #变量
        y=data.Income    #因变量

        model=tf.keras.Sequential()#顺序模型的初始化（Sequential）
        #在模型中添加Dense层 （#输出数据维度 #输入数据的形状）
        model.add(tf.keras.layers.Dense(1,input_shape=(1,)))
        model.summary()#反应model的整体形状

        #编译过程也就是配置，使用(梯度下降算法)对（损失函数）进行优化
        #optimizer就是一种优化方法，这种优化算法会计算梯度，沿着梯度下降的方向，去改变变量的值，从而求（输出变量）的最小值
        #'mse' means 均方差
        model.compile(optimizer='adam', loss='mse')

        #进行训练，epochs means 对所有变量进行训练的次数
        history=model.fit(x,y,epochs=5000)

        Q=model.predict(x)
        print(Q)

        # W=model.predict(pd.Series([20]))
        # print(W)

        plt.scatter(data.Education, data.Income ,color = "red")
        plt.scatter(x, Q, color = "blue")
        plt.show()
