# DeepEdge
Performance Evaluation of Deep Learning Models on Edge Devices - **Devices/Models need to be updated**

Models will be updated by `Srujana Malisetti` (below is the current models as of Mar/20/2020)
 - `Tensorflow`: MobileNet V2
 - `MxNet`: MobileNet V1, Densenet 161, Squeezenet V1, AlexNet, ResNet18, Inception v3
 - `PyTorch`: MobileNet V2 (v1 is trying), Densenet161, SqueezenetV1, AlexNet, ResNet 18, GoogleNet, ShuffleNet


Device Specifications
| Device | OS | CPU | MEM | GPU/Accelerator | Storage | Qty | Memo | 
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Atomic Pi](https://hackaday.com/2019/06/06/the-atomic-pi-is-it-worth-it/)  | Ubuntu 18.04 | [Intel Atom x5-Z8350 quad core](https://en.wikichip.org/wiki/intel/atom_x5/x5-z8350)<BR>with 2M Cache | 2GB RAM, 16GB eMMC | 480MHz GPU | SD slot<BR>(up to 32GB) | 1 + 1 | User:atomicpi Password: atomicpi123|
| [Raspberry Pi4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/) | Raspbian9 | [Cortex A-72 proccessor](https://en.wikipedia.org/wiki/ARM_Cortex-A72),<BR>64 Bit Quad core | 4GB RAM | -- | Micro SD slot<BR>(upto 32G) | 2+ | Password: raspberry|
| [Odroid N2](https://www.hardkernel.com/blog-2/odroid-n2/) | Android 9.0(Pie) | [Amlogic S922X Processor (12nm)](https://en.wikipedia.org/wiki/Amlogic),<BR>Quad-core Cortex-A73(1.8Ghz) and Dual-core Cortex-A53(1.9Ghz) | 4GB RAM | [Mali-G52 GPU](https://developer.arm.com/ip-products/graphics-and-multimedia/mali-gpus/mali-g52-gpu) | Micro SD slot<BR>(32 GB) | 2 |Playstore Credentials: Email Id : odroidn2.deepedge@gmail.com <BR> Password:DeepEdge123$%|
| [Odroid C2](https://www.hardkernel.com/shop/odroid-c2/) | Android 6.0 (Marshmallow) | Amlogic [ARM Cortex-A53 (ARMv8)](https://en.wikipedia.org/wiki/ARM_Cortex-A53) 1.5Ghz quad core CPUs | 2GB RAM | [Mali-450 GPU](https://developer.arm.com/ip-products/graphics-and-multimedia/mali-gpus/mali-450-gpu) | Micro SD slot<BR>(16 GB) | 1 |Playstore Credentials: Email Id : deepedge.ugacs@gmail.com <BR> Password:Deepedge123$% |
| [Coral Dev Board](https://coral.ai/docs/dev-board/datasheet/) | Mendel Linux | [NXP i.MX 8M SoC](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i.mx-applications-processors/i.mx-8-processors/i.mx-8m-family-armcortex-a53-cortex-m4-audio-voice-video:i.MX8M)<sub>[[1]](https://en.wikipedia.org/wiki/I.MX#i.MX_8M)</sub>,<BR>Quad Cortex-A53, Cortex-M4F | 1GB RAM, 8 GB eMMC | [Google Edge TPU ML accelerator](https://coral.ai/docs/accelerator/datasheet/),<BR>Integrated GC7000 Lite Graphics | -- | 2 | |
| [Edge TPU coprocessor](https://coral.ai/products/accelerator) | -- | -- | -- | TPU ML accelerator | -- | 2 | |
| [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) <sub>[[1]](https://developer.nvidia.com/embedded/develop/hardware)</sub> | Ubuntu18.04 | Quad-core ARM A57 @ 1.43 GHz | 4 GB 64-bit LPDDR4 25.6 GB/s | 128-core Maxwell | microSD (128 GB) | 2 | Power: 5W / 10W<BR> user: jnano; password:jetson |
| [Jetson TX2](https://developer.nvidia.com/embedded/jetson-tx2) | -- | [Dual-Core NVIDIA Denver 2 64-Bit CPU](https://devblogs.nvidia.com/jetson-tx2-delivers-twice-intelligence-edge/),<BR>Quad-Core ARM® Cortex®-A57 MPCore | 8GB 128-bit LPDDR4 Mem<BR>1866 MHx - 59.7 GB/s | 256-core NVIDIA [Pascal<sup>™</sup>](https://developer.nvidia.com/pascal) GPU architecture with 256 NVIDIA CUDA cores | 32GB eMMC 5.1 |  1 | Power: 7.5W / 15W |

<!-- 1. [Atomic Pi](https://hackaday.com/2019/06/06/the-atomic-pi-is-it-worth-it/) :
CPU : [Intel Atom x5-Z8350 quad core](https://en.wikichip.org/wiki/intel/atom_x5/x5-z8350) with 2M Cache, 480MHz GPU, 
Memory: 2GB RAM, 16GB eMMC, SD slot for adding memory(32GB) 
2. [Raspberry Pi4 ModelB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/):
CPU: Cortex A-72 proccessor, 64 Bit Quad core 
Memory: 4GB RAM, Micro SD slot for adding more memory(32GB)
3. [Odroid N2](https://www.hardkernel.com/blog-2/odroid-n2/): 
CPU: [Amlogic S922X Processor (12nm)](https://en.wikipedia.org/wiki/Amlogic), Quad-core Cortex-A73(1.8Ghz) and Dual-core Cortex-A53(1.9Ghz), Mali-G52 GPU
Memory: 4GBRAM, Micro SDslot(32 GB)
4. [Coral Dev Board](https://coral.ai/docs/dev-board/datasheet/):
CPU: NXP i.MX 8M SoC Quad Cortex-A53,Cortex-M4F  
Memory: 1GB RAM, 8 GB eMMC, 
GPU: Integrated GC7000 Lite Graphics
5. [Google Edge TPU coprocessor](https://coral.ai/products/accelerator)
 -->

**Model Repo**
- https://drive.google.com/drive/folders/1exwYFgbGqT7iRw--WlB1xixcIFwzvNWy?usp=sharing

**TODO List** (Do not delete)
0. Additional Parameter -- `Startup Time`.
1. Android on Odroid N2 because the CPU is used for Android TV.
2. More devices [[1]](https://www.electromaker.io/blog/article/10-best-raspberry-pi-alternatives), [[2]](https://www.ubuntupit.com/best-raspberry-pi-alternatives/), [[3]](https://all3dp.com/1/single-board-computer-raspberry-pi-alternative/)
3. Finalize Models for General Deep Learning and ones that designed for mobile devices
4. Dataset for evaluation - Image Classification: [MNIST](http://yann.lecun.com/exdb/mnist/), [CIFAR](https://www.cs.toronto.edu/~kriz/cifar.html), [ImageNet](http://www.image-net.org/), Q&A Dataset: [SQuAD2.0](https://rajpurkar.github.io/SQuAD-explorer/explore/1.1/dev/), and more (e.g., text classification)
5. Performance Metrics - System metrics for singe/batch execution, ML metrics (e.g., TOP-5 accuracy), refer to [[1]](https://dawn.cs.stanford.edu/benchmark/)
6. Power Measuring Device - [INA219](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout)
7. If direct installation is too difficult for specific boards, please try -- [HPE Deep Learning Benchmark](https://hewlettpackard.github.io/dlcookbook-dlbs/#/), [Stanford DAWN Benchmark](https://dawn.cs.stanford.edu/benchmark/#squad), [ML Perf](https://mlperf.org/)
8. Reading List
   - [MLPerf Inference Benchmark](https://arxiv.org/abs/1911.02549)
   - https://mlperf.org/
   - (IC2E 2020) [Perseus: Characterizing Performance and Cost of Multi-Tenant Serving for CNN Models](https://arxiv.org/abs/1912.02322)
   - [SMAUG: End-to-End Full-Stack Simulation Infrastructure for Deep Learning Workloads](https://arxiv.org/abs/1912.04481)

**SDKs**
1. DeepStream - https://developer.nvidia.com/deepstream-sdk
   - https://bit.ly/3bLCro4 -- DeepStream + AutoML + Jetson Nano Deployment
2. Google Cloud AutoML - https://cloud.google.com/automl
3. NVidia Docker Container - https://github.com/NVIDIA/nvidia-docker
