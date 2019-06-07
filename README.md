# FIVR-200K
An annotated dataset of YouTube videos designed as a benchmark for Fine-grained Incident Video Retrieval. The dataset comprises 225,960 videos associated with 4,687 Wikipedia events and 100 selected video queries. 

Project Website: [[link](http://ndd.iti.gr/fivr/)]

Paper: [[publisher](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8668422)] [[arXiv](https://arxiv.org/abs/1809.04094)] [[pdf](https://arxiv.org/pdf/1809.04094.pdf)]

## Installation

* Clone this repo:
```bash
git clone https://github.com/MKLab-ITI/ndvr-dml
cd ndvr-dml
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