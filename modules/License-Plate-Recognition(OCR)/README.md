# **LPRnet을 이용한 대한민국 자동차 번호판 인식**
---------
This repository is based on the paper  [LPRNet: License Plate Recognition via Deep Neural Networks](https://arxiv.org/pdf/1806.10447.pdf). 
We use the [KarPlate Dataset](http://pr.gachon.ac.kr/ALPR.html) for training and test model

## **요구사항**
- Python 3.6+
- Tensorflow 1.15 or 2
- Opencv 4
- tqdm
- editdistance

## **사용법**
### *데이터 셋*
[data.zip](https://bit.ly/3egQ9jU), 압축을 푼 후 **data** 폴더에 이동 후 테스트 및 학습

### *Pre-trained model*
[best_weights.zip](https://bit.ly/2zt5hMc), 압축을 푼 후 **pre_trained** 폴더에 이동 후 테스트


--------

### *Demo*
```bash
python predict.py -i data/test_images/4.jpg -w pre_trained/weights_best.pb
```

### *Training*
```bash
python train.py -l data/label.json -i data/train_images --valid_label data/test.json --valid_img_dir data/test_images --save_weights_only --load_all 
```

### *Testing*
```bash
python predict.py -i data/test_images/4.jpg -w saved_models/weights_best.pb
```

### *Evaluate*
```bash
python evaluate.py -l data/test.json -i data/test_images/ -w saved_models/weights_best.pb
```


--------

# *result*

![image](https://user-images.githubusercontent.com/68686603/126833975-8bcfe13e-3a26-44ad-8262-6d59e2001f67.png)

![image](https://user-images.githubusercontent.com/68686603/126833997-9233e9cf-0d18-48ec-8c9b-baf43749e769.png)

![image](https://user-images.githubusercontent.com/68686603/126834026-3cb46e53-49e9-4e87-95b0-672180362236.png)
