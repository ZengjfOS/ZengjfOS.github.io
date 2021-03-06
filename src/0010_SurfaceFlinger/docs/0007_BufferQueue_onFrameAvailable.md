# BufferQueue onFrameAvailable

BufferQueueProducer的queueBuffer()工作流程

# 参考文档

* [SurfaceFlinger学习之路（三）BufferQueue原理](https://blog.csdn.net/qq_15893929/article/details/102813185)
* [Android Q SurfaceFlinger合成（一）](https://wizzie.top/Blog/2020/10/15/2020/201015_android_SurfaceFlinger1/)

# onFrameAvailable

```
* frameworks/native/libs/gui/BufferQueueProducer.cpp
  * status_t BufferQueueProducer::queueBuffer(int slot, const QueueBufferInput &input, QueueBufferOutput *output) 
    * frameAvailableListener = mCore->mConsumerListener;
    * if (frameAvailableListener != nullptr)
      * frameAvailableListener->onFrameAvailable(item);
        * frameworks/native/libs/gui/BufferQueue.cpp
          * void BufferQueue::ProxyConsumerListener::onFrameAvailable(const BufferItem& item)
            * sp<ConsumerListener> listener(mConsumerListener.promote());
            * listener->onFrameAvailable(item);
              * frameworks/native/libs/gui/ConsumerBase.cpp
                * void ConsumerBase::onFrameAvailable(const BufferItem& item)
                  * listener = mFrameAvailableListener.promote();
                  * listener->onFrameAvailable(item);
                    * frameworks/native/services/surfaceflinger/BufferQueueLayer.cpp
                      * void BufferQueueLayer::ContentsChangedListener::onFrameAvailable(const BufferItem& item)
                        * mBufferQueueLayer->onFrameAvailable(item);
                          * void BufferQueueLayer::onFrameAvailable(const BufferItem& item)
                            * mFlinger->signalLayerUpdate();
                              * frameworks/native/services/surfaceflinger/SurfaceFlinger.cpp
                                * mEventQueue->invalidate();
                                  * frameworks/native/services/surfaceflinger/Scheduler/MessageQueue.cpp
                                    * void MessageQueue::invalidate()
                                      * mInjector.connection->requestNextVsync();
                                        * frameworks/native/services/surfaceflinger/Scheduler/EventThread.cpp
                                          * void EventThreadConnection::requestNextVsync()
                                            * mEventThread->requestNextVsync(this);
                                              * frameworks/native/services/surfaceflinger/Scheduler/EventThread.cpp
                                                * void EventThread::requestNextVsync(const sp<EventThreadConnection>& connection)
                                                  * mCondition.notify_all();
                            * mConsumer->onBufferAvailable(item);
```
