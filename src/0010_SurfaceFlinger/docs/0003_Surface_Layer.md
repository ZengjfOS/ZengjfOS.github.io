# Surface Layer

Surface和Layer的概念

# 参考文档

* [Android画面显示流程分析(5)](https://www.jianshu.com/p/dcaf1eeddeb1)
* [AndroidQ 图形系统（2）生产者-消费者模型](https://blog.csdn.net/qq_34211365/article/details/106503902)
* [Android图形显示系统6　图像缓冲区(下)](https://blog.csdn.net/liuwg1226/article/details/115385299)
* [SurfaceFlinger学习之路（三）BufferQueue原理](https://blog.csdn.net/qq_15893929/article/details/102813185)

# Surface Layer

* Layer是一个图层
* Surface实际显示在手机上的某一个图像，这个图像可能由多个Layer组成

# Vsync-app 跟 Vsync-sf

* VSYNC-app用于控制APP绘制UI的节奏，其实就是SF中app-DispSyncSource根据自己需要，转发DispSync的sync信号。
* VSYNC-sf用于控制SF合成Layer的节奏，可以理解为sf对应的DispSyncSource发出的sync信号，再触发EventThread的回调并转换成事件写入写端，最后触发读端的回调MessageQueue::cb_eventReceiver()，SF开始合成显示图层

# example

```CPP
int main()
{
    sp<ProcessState> proc(ProcessState::self());
    ProcessState::self()->startThreadPool();//在应用和SurfaceFlinger沟通过程中要使用到binder, 所以这里要先初始化binder线程池

    sp<SurfaceComposerClient> client = new SurfaceComposerClient();//SurfaceComposerClient是SurfaceFlinger在应用侧的代表， SurfaceFlinger的接口通过它来提供
    client->initCheck();
    //先通过createSurface接口来申请一块画布，参数里包含对画布起的名字，大小，位深信息
    sp<SurfaceControl> surfaceControl = client->createSurface(String8("Console Surface"),800, 600, PIXEL_FORMAT_RGBA_8888);

    SurfaceComposerClient::Transaction t;
    t.setLayer(surfaceControl, 0x40000000).apply();
    //通过getSurface接口获取到Surface对象
    sp<Surface> surface = surfaceControl->getSurface();
    
    ANativeWindow_Buffer buffer;
    //通过Surface的lock方法调用到dequeueBuffer，获取到一个BufferQueue可用的Slot
    status_t err = surface->lock(&buffer, NULL);// &clipRegin

    void* addr = buffer.bits;
    ssize_t len = buffer.stride * 4 * buffer.height;
    memset(addr, 255, len);//这里绘图，由于我们没有使用任何图形库，所以这里把内存填成255， 画一个纯色画面
    
    surface->unlockAndPost();//这里会调用到queueBuffer,把我们绘制好的画面提交给SurfaceFlinger

    printf("sleep...\n");
    usleep(5 * 1000 * 1000);
    
    surface.clear();
    surfaceControl.clear();
    
    printf("complete. CTRL+C to finish.\n");
    IPCThreadState::self()->joinThreadPool();
    return 0;
}
```

# SurfaceComposerClient

* SurfaceComposerClient对应的SF Server端就是Client实例

```
* frameworks/native/libs/gui/include/gui/SurfaceComposerClient.h
  * class SurfaceComposerClient : public RefBase
    * SurfaceComposerClient();
      * frameworks/native/libs/gui/SurfaceComposerClient.cpp
        * SurfaceComposerClient::SurfaceComposerClient() : mStatus(NO_INIT) {}
    * void SurfaceComposerClient::onFirstRef()
      * sp<ISurfaceComposer> sf(ComposerService::getComposerService());
      * sp<ISurfaceComposerClient> conn;
      * conn = sf->createConnection();
        * frameworks/native/services/surfaceflinger/SurfaceFlinger.cpp
          * sp<ISurfaceComposerClient> SurfaceFlinger::createConnection()
            * const sp<Client> client = new Client(this);
              * frameworks/native/services/surfaceflinger/Client.cpp
                * Client::Client(const sp<SurfaceFlinger>& flinger) : mFlinger(flinger)
                  * frameworks/native/services/surfaceflinger/Client.h
                    * class Client : public BnSurfaceComposerClient
                      * SurfaceComposerClient对应的SF Server端就是Client实例
            * return client->initCheck() == NO_ERROR ? client : nullptr;
```

# createSurface

* SurfaceComposerClient通过对应的Client发起createSurface()请求，最终转换成createLayer()处理；
* 默认创建的BufferQueueLayer，当然还有其他的Layer；
* BufferQueueLayer其内部包含了BufferQueue；
* BufferQueue其内部包含了BufferQueueCore、BufferQueueProducer、BufferQueueConsumer；
* 返回的SurfaceControl就是BufferQueue控制器；
* 其实这里的本质是创建了BufferQueue；

```
* frameworks/native/services/surfaceflinger/Client.cpp
  * status_t Client::createSurface(...)
    * return mFlinger->createLayer(name, this, w, h, format, flags, std::move(metadata), handle, gbp, parentHandle, outLayerId, nullptr, outTransformHint);
      * frameworks/native/services/surfaceflinger/SurfaceFlinger.cpp
        * status_t SurfaceFlinger::createLayer(...)
          * switch (flags & ISurfaceComposerClient::eFXSurfaceMask)
            * case ISurfaceComposerClient::eFXSurfaceBufferQueue:
              * result = createBufferQueueLayer(client, std::move(uniqueName), w, h, flags, std::move(metadata), format, handle, gbp, &layer);
                * LayerCreationArgs args(this, client, std::move(name), w, h, flags, std::move(metadata));
                * args.textureName = getNewTexture();
                * layer = getFactory().createBufferQueueLayer(args);
                  * frameworks/native/services/surfaceflinger/SurfaceFlingerDefaultFactory.cpp
                    * sp<BufferQueueLayer> DefaultFactory::createBufferQueueLayer(const LayerCreationArgs& args)
                      * return new BufferQueueLayer(args);
                        * frameworks/native/services/surfaceflinger/BufferQueueLayer.h
                          * class BufferQueueLayer : public BufferLayer
                            * BufferQueueLayer::BufferQueueLayer(const LayerCreationArgs& args) : BufferLayer(args) 
                            * void BufferQueueLayer::onFirstRef()
                              * BufferLayer::onFirstRef();
                                * sp<IGraphicBufferProducer> producer;
                                * sp<IGraphicBufferConsumer> consumer;
                                * mFlinger->getFactory().createBufferQueue(&producer, &consumer, true);
                                  * frameworks/native/services/surfaceflinger/SurfaceFlingerDefaultFactory.cpp
                                    * void DefaultFactory::createBufferQueue(sp<IGraphicBufferProducer>* outProducer, sp<IGraphicBufferConsumer>* outConsumer, bool consumerIsSurfaceFlinger)
                                      * BufferQueue::createBufferQueue(outProducer, outConsumer, consumerIsSurfaceFlinger);
                                        * frameworks/native/libs/gui/BufferQueue.cpp
                                          * sp<BufferQueueCore> core(new BufferQueueCore());
                                            * frameworks/native/libs/gui/include/gui/BufferQueueCore.h
                                              * BufferQueueDefs::SlotsType mSlots;
                                                * frameworks/native/libs/gui/include/gui/BufferQueueDefs.h
                                                  * typedef BufferSlot SlotsType[NUM_BUFFER_SLOTS];
                                                    * frameworks/native/libs/gui/include/gui/BufferSlot.h
                                                      * struct BufferSlot
                                                        * sp<GraphicBuffer> mGraphicBuffer;
                                          * sp<IGraphicBufferProducer> producer(new BufferQueueProducer(core, consumerIsSurfaceFlinger));
                                            * frameworks/native/libs/gui/include/gui/BufferQueueProducer.h
                                              * class BufferQueueProducer : public BnGraphicBufferProducer, private IBinder::DeathRecipient
                                          * sp<IGraphicBufferConsumer> consumer(new BufferQueueConsumer(core));
                                            * frameworks/native/libs/gui/include/gui/BufferQueueConsumer.h
                                              * class BufferQueueConsumer : public BnGraphicBufferConsumer
                                          * *outProducer = producer;
                                          * *outConsumer = consumer;
                                * mProducer = mFlinger->getFactory().createMonitoredProducer(producer, mFlinger, this);
                                * mConsumer = mFlinger->getFactory().createBufferLayerConsumer(consumer, mFlinger->getRenderEngine(), mTextureName, this);
                * status_t err = layer->setDefaultBufferProperties(w, h, format);
                * *handle = layer->getHandle();
                  * frameworks/native/services/surfaceflinger/Layer.cpp
                    * return new Handle(mFlinger, this);
                      * frameworks/native/services/surfaceflinger/Layer.h
                        * class Handle : public BBinder, public LayerCleaner
                * *gbp = layer->getProducer();
                * *outLayer = layer;
          * result = addClientLayer(client, *handle, *gbp, layer, parentHandle, parentLayer, addToRoot, outTransformHint);
            * 函数addClientLayer将创建的Layer保存到当前State的Z秩序列表
          * mInterceptor->saveSurfaceCreation(layer);
```

# GraphicBuffer

GraphicBuffer 是图像缓冲区的最后一个组成部分，也是最基本最重要的一个单元，在前面讲到 BufferQueueProucer 通过 dequeueBuffer 获取 BufferSlot 时，会判断 BufferSlot 中的 GraphicBuffer 是否为空，如果为空就会创建新的 GraphicBuffer。

```
* frameworks/native/libs/gui/BufferQueueProducer.cpp
  * status_t BufferQueueProducer::dequeueBuffer(...)
    * if (returnFlags & BUFFER_NEEDS_REALLOCATION)
      * sp<GraphicBuffer> graphicBuffer = new GraphicBuffer(width, height, format, BQ_LAYER_COUNT, usage, {mConsumerName.string(), mConsumerName.size()});
        * status_t error = graphicBuffer->initCheck();
          * frameworks/native/libs/ui/GraphicBuffer.cpp
            * mInitCheck = initWithSize(inWidth, inHeight, inFormat, inLayerCount, inUsage, std::move(requestorName));
              * GraphicBufferAllocator& allocator = GraphicBufferAllocator::get();
              * status_t err = allocator.allocate(inWidth, inHeight, inFormat, inLayerCount, inUsage, &handle, &outStride, mId, std::move(requestorName));
```

# getSurface

从理论上来讲Surface本质是mGraphicBufferProducer，因为它才是提供缓存的本质

```
* sp<Surface> surface = surfaceControl->getSurface();
  * frameworks/native/libs/gui/SurfaceControl.cpp
    * sp<Surface> SurfaceControl::getSurface()
      * mSurfaceData = new Surface(mGraphicBufferProducer, false);
```
