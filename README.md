# J-RESRGAN 

This is a fork of https://github.com/xinntao/Real-ESRGAN with some **modifications** to perform super-resolution enhancement specifically for **J-Resolved NMR spectral data**.

## Dependencies, Installation & Usage

- Python >= 3.7 (Recommend to use [Anaconda](https://www.anaconda.com/download/#linux) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- [PyTorch >= 1.7](https://pytorch.org/)

### Installation

1. Clone repo

    ```bash
    git clone https://github.com/yanyan5420/Real-ESRGAN.git
    cd Real-ESRGAN
    ```

2. Install dependent packages

    ```bash
    # Install the modified basicsr - https://github.com/yanyan5420/BasicSR
    # We use BasicSR for both training and inference
    pip install git+https://github.com/yanyan5420/BasicSR.git
    pip install -r requirements.txt
    python setup.py develop
    ```

### Inference J-Res Spectra
1. Download pre-trained model: [JRESRGAN_x2plus.pth](https://github.com/yanyan5420/Real-ESRGAN/releases/download/v1.0.0/JRESRGAN_x2plus.pth) 

```bash
wget https://github.com/yanyan5420/Real-ESRGAN/releases/download/v1.0.0/JRESRGAN_x2plus.pth -P weights
```

2. Inference:
First, put a J-Res spectrum into `inputs` folder; and run the command:

```bash
python inference_realesrgan.py -n JRESRGAN_x2plus -i inputs -s 2

Common command options:
  -h                   show this help
  -i --input           Input image or folder. Default: inputs
  -o --output          Output folder. Default: results
  -n --model_name      Model name. Default: JRESRGAN_x2plus
  -s, --outscale       The final upsampling scale of the image. Default: 2
  -t, --tile           Tile size, 0 for no tile during testing. Default: 0
  --fp32               Use fp32 precision during inference. Default: fp16 (half precision).
```
Outputs will show in the `results` folder.


## Online Inference

You can use the [Online Inference Demo](https://colab.research.google.com/drive/1bZxpI5zzAqq1uJ6QpwEGTS6xXjhYOnW_?usp=sharing) to get a quick inference. 


## Contact

If you have any question, please email `y.yan20@imperial.ac.uk`.


## 🤗 Acknowledgement
