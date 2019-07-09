# FIVR-200K
<img src="https://raw.githubusercontent.com/MKLab-ITI/FIVR-200K/master/banner.png" width="100%">

An annotated dataset of YouTube videos designed as a benchmark for Fine-grained Incident Video Retrieval. The dataset comprises 225,960 videos associated with 4,687 Wikipedia events and 100 selected video queries. 

Project Website: [[link](http://ndd.iti.gr/fivr/)]

Paper: [[publisher](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8668422)] [[arXiv](https://arxiv.org/abs/1809.04094)] [[pdf](https://arxiv.org/pdf/1809.04094.pdf)]

## Installation

* Clone this repo:
```bash
git clone https://github.com/MKLab-ITI/FIVR-200K
cd FIVR-200K
```
* You can install all the dependencies by
```bash
pip install -r requirements.txt
```
or
```bash
conda install --file requirements.txt
```
* Install [Youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) (make sure it is up-to-date)

## Dataset format

* The files that contains the dataset can be found in the [dataset](https://github.com/MKLab-ITI/FIVR-200K/tree/master/dataset) folder

* The video annotations are in the file [annotation.json](https://github.com/MKLab-ITI/FIVR-200K/blob/master/dataset/annotation.json) that has the following format:
```bash
{
  "5MBA_7vDhII": {
    "ND": [
      "_0uCw0B2AgM",
      ...],
    "DS": [
      "hc0XIE1aY0U",
      ...],
    "CS": [
      "ydEqiuDiuyc",
      ...],    
    "IS": [
      "d_ZNjE7B4Wo",
      ...]
  },
  ....
}
```

* The events crawled from [Wikipedia](https://en.wikipedia.org/wiki/Portal:Current_events) are in the file [events.json](https://github.com/MKLab-ITI/FIVR-200K/blob/master/dataset/events.json) that has the following format:
```bash
[
  {
    "headline": "iraqi insurgency", 
    "topic": "armed conflict and attack", 
    "date": "2013-01-22", 
    "text": [
      "car bombings in baghdad kill at least 17 people and injure dozens of others."
    ], 
    "href": [
      "http://www.bbc.co.uk/news/world-middle-east-21141242", 
      "https://www.reuters.com/article/2013/01/22/us-iraq-violence-idUSBRE90L0BQ20130122"
    ], 
    "youtube": [
      "ZpjqUq-EnbQ", 
      ...
    ]
  },
  ...
]
```

* The Youtube IDs of the videos in the dataset are in the file [youtube_ids.txt](https://github.com/MKLab-ITI/FIVR-200K/blob/master/dataset/youtube_ids.txt)

## Download Videos

* Run the following command to download videos:
```bash
python download_dataset.py --video_dir VIDEO_DIR [--dataset_ids DATASET_FILE] [--cores NUMBER_OF_CODES] [--resolution RESOLUTION]
```

* An example to run the download script:
```bash
python download_dataset.py --video_dir ./videos --dataset_ids dataset/youtube_ids.txt --cores 4 --resolution 360
```

* Videos will be saved in the following directory structure ```VIDEO_DIR/YT_ID.mp4```

* The videos that are no longer available are stored in a text file with name ```missing_videos.txt```


## Citation
If you use this code for your research, please cite our paper.
```
@article{kordopatis2019fivr,
  title={FIVR: Fine-grained Incident Video Retrieval},
  author={Kordopatis-Zilos, Giorgos and Papadopoulos, Symeon and Patras, Ioannis and Kompatsiaris, Ioannis},
  journal={IEEE Transactions on Multimedia},
  year={2019}
}
```

## Related Projects
**[NDVR-DML](https://github.com/MKLab-ITI/ndvr-dml)** **[Intermediate-CNN-Features](https://github.com/MKLab-ITI/intermediate-cnn-features)**

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## Contact for further details about the project

Giorgos Kordopatis-Zilos (georgekordopatis@iti.gr) <br>
Symeon Papadopoulos (papadop@iti.gr)