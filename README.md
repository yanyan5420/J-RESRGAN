# J-RESRGAN 

This is a fork of https://github.com/xinntao/Real-ESRGAN with some **modifications** to perform super-resolution enhancement specifically for **J-Resolved NMR spectral data**.

## Dependencies and Installation

- Python >= 3.7 (Recommend to use [Anaconda](https://www.anaconda.com/download/#linux) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- [PyTorch >= 1.7](https://pytorch.org/)

### Installation

1. Clone repo

    ```bash
    git clone https://github.com/yanyan5420/Real-ESRGAN.git
    cd Real-ESRGAN
    ```

1. Install dependent packages

    ```bash
    # Install the modified basicsr - https://github.com/yanyan5420/BasicSR
    # We use BasicSR for both training and inference
    pip install git+https://github.com/yanyan5420/BasicSR.git
    pip install -r requirements.txt
    python setup.py develop
    ```

## Online Inference

You can use the [Online Inference Demo](https://colab.research.google.com/drive/1bZxpI5zzAqq1uJ6QpwEGTS6xXjhYOnW_?usp=sharing) to get a quick inference. 


## Contact

If you have any question, please email `y.yan20@imperial.ac.uk`.


## 🤗 Acknowledgement
