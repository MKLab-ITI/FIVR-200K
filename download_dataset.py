# Copyright 2019 Giorgos Kordopatis-Zilos. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
Script that downloads the videos in the FIVR-200K dataset
"""

from __future__ import division
from __future__ import print_function

import os
import argparse
import yt_dlp
import numpy as np

from tqdm import tqdm
from multiprocessing import Pool


def download_video(video_id, args):
    """
      Download the provided video using the yt-dlp library

      Args:
        video_id: Youtube ID of the video
        args: arguments provided by the user
      Returns:
        a flag that indicates whether there was an error during the downloading
    """
    try:
        ydl_opts = {
                'format': 'best[height<={}][ext=mp4]/best[ext=mp4]/best[height<={}]/best'
                    .format(args.resolution, args.resolution),
                'outtmpl': '{}/{}.%(ext)s'.format(args.video_dir, video_id),
                'quiet': True,
                'no_warnings': True
            }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        video_url = video_id if 'http' not in video_id else 'https://www.youtube.com/watch?v={}'.format(video_id)
        ydl.download([video_url])
        return True
    except:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video_dir',
                        required=True,
                        help='Directory where the downloaded videos will be stored')
    parser.add_argument('-d', '--dataset_ids',
                        default='dataset/youtube_ids.txt',
                        help='File that contains the Youtube IDs of the videos in FIVR-200K dataset')
    parser.add_argument('-c', '--cores',
                        default=8, type=int,
                        help='Number of cores that will be used for downloading.')
    parser.add_argument('-r', '--resolution',
                        default=480, type=int,
                        help='Preferred resolution to download videos.')
    args = parser.parse_args()

    # create root dir
    if not os.path.exists(args.video_dir):
        os.makedirs(args.video_dir)

    dataset = np.loadtxt(args.dataset_ids, dtype=str)
    missing_videos = set(np.loadtxt('missing_videos.txt', dtype=str)) \
        if os.path.exists('missing_videos.txt') else set()
    with open('missing_videos.txt', 'a') as f:
        progress_bar = tqdm(dataset)
        if args.cores > 1:
            future = []
            pool = Pool(args.cores)
            for video in dataset:
                future.append(pool.apply_async(download_video, args=[video, args],
                                               callback=(lambda *a: progress_bar.update())))

            for video, flag in zip(dataset, future):
                if not flag.get() and video not in missing_videos:
                    f.write('{}\n'.format(video))
                    f.flush()
                    missing_videos.add(video)
            pool.terminate()
        else:
            for video in progress_bar:
                flag = download_video(video, args)
                if not flag and video not in missing_videos:
                    f.write('{}\n'.format(video))
                    f.flush()
    print('Downloading completed!')
