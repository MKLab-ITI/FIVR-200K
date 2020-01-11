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
Implementation of the FIVR evaluation process
"""

from __future__ import division
from __future__ import print_function

import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from argparse import RawTextHelpFormatter
from future.utils import viewitems, lrange
from sklearn.metrics import precision_recall_curve


def plot_pr_curve(pr_curve):
    """
      Function that plots the interpolated PR-curve.

      Args:
        pr_curve: the values of precision for each recall step
    """
    plt.figure(figsize=(16, 9))
    plt.plot(np.arange(0.0, 1.05, 0.05),
             pr_curve, color='r', marker='o', linewidth=3, markersize=10)
    plt.grid(True, linestyle='dotted')
    plt.xlabel('Recall', color='k', fontsize=27)
    plt.ylabel('Precision', color='k', fontsize=27)
    plt.yticks(color='k', fontsize=20)
    plt.xticks(color='k', fontsize=20)
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.tight_layout()
    plt.show()


def evaluate(annotations, results, relevant_labels, dataset, quiet):
    """
      Calculate of mAP and interpolated PR-curve based on the FIVR evaluation process.

      Args:
        annotations: the annotation labels for each query
        results: the similarities of each query with the videos in the dataset
        relevant_labels: labels that are considered positives
        dataset: video ids contained in the dataset
      Returns:
        mAP: the mean Average Precision
        ps_curve: the values of the PR-curve
    """
    pr, mAP = [], []
    iterations = viewitems(annotations) if not quiet else tqdm(viewitems(annotations))
    for query, gt_sets in iterations:
        if query not in results: print('WARNING: Query {} is missing from the result file'.format(query)); continue
        if query not in dataset: print('WARNING: Query {} is not in the dataset'.format(query)); continue

        # set of relevant videos
        query_gt = set(sum([gt_sets[label] for label in relevant_labels if label in gt_sets], []))
        query_gt = query_gt.intersection(dataset)
        if not query_gt: print('WARNING: Empty annotation set for query {}'.format(query)); continue

        # calculation of mean Average Precision (Eq. 6)
        i, ri, s = 0.0, 0, 0.0
        y_target, y_score = [], []
        for video, sim in sorted(viewitems(results[query]), key=lambda x: x[1], reverse=True):
            if video != query and video in dataset:
                y_score.append(sim)
                y_target.append(1.0 if video in query_gt else 0.0)
                ri += 1
                if video in query_gt:
                    i += 1.0
                    s += i / ri
        mAP.append(s / len(query_gt))
        if not quiet:
            print('Query:{}\t\tAP={:.4f}'.format(query, s / len(query_gt)))

        # add the dataset videos that are missing from the result file
        missing = len(query_gt) - y_target.count(1)
        y_target += [1.0 for _ in lrange(missing)] # add 1. for the relevant videos
        y_target += [0.0 for _ in lrange(len(dataset) - len(y_target))] # add 0. for the irrelevant videos
        y_score += [0.0 for _ in lrange(len(dataset) - len(y_score))]

        # calculation of interpolate PR-curve (Eq. 5)
        precision, recall, thresholds = precision_recall_curve(y_target, y_score)
        p = []
        for i in lrange(20, -1, -1):
            idx = np.where((recall >= i * 0.05))[0]
            p.append(np.max(precision[idx]))
        pr.append(p)

    return mAP, np.mean(pr, axis=0)[::-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-r', '--result_file',
                        required=True,
                        help='File of where the results are stored. It must be in JSON format')
    parser.add_argument('-rl', '--relevant_labels',
                        default='ND,DS',
                        help='Labels of the videos that considered relevant depending on the retrieval task'
                             '\nDSVR: ND,DS\nCSVR: ND,DS,CS\nISVR: ND,DS,CS,IS')
    parser.add_argument('-a', '--annotations_file',
                        default='dataset/annotation.json',
                        help='File that contains the video annotations of the FIVR-200K dataset')
    parser.add_argument('-d', '--dataset_ids',
                        default='dataset/youtube_ids.txt',
                        help='File that contains the Youtube IDs of the videos in FIVR-200K dataset')
    parser.add_argument('-e', '--export_file',
                        default='mAP_PRcurve_points.csv',
                        help='File where the results will be stored')
    parser.add_argument('-s', '--save_results',
                        action='store_true',
                        help='Flag that indicated whether the results will be stored')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Flag that indicated whether the results per query will be printed')
    parser.add_argument('-p', '--plot_pr_curve',
                        action='store_true',
                        help='Flag that indicated whether the PR-curve will be displayed')
    args = parser.parse_args()

    # load all the necessary files
    with open(args.result_file, 'r') as f:
        if not args.quiet: print('Loading results from file:', args.result_file)
        results = json.load(f)
    with open(args.annotations_file, 'r') as f:
        if not args.quiet: print('Loading annotations from file:', args.annotations_file)
        annotations = json.load(f)
    dataset = set(np.loadtxt(args.dataset_ids, dtype=str))
    relevant_labels = args.relevant_labels.split(',')

    # run the evaluation process
    mAP, pr_curve = evaluate(annotations, results, relevant_labels, dataset, args.quiet)

    # report the results
    print('==========================================')
    print('Total queries: {}\t\tmAP={:.4f}'.format(len(mAP), np.mean(mAP)))
    if args.plot_pr_curve: plot_pr_curve(pr_curve)

    # save the numeric values in a csv file
    if args.save_results:
        with open(args.export_file, 'w') as f:
            f.write('mAP,{}\n\n'.format(np.mean(mAP)))
            f.write('Recall,{}\n'.format(','.join(map(str, np.arange(0.0, 1.05, 0.05)))))
            f.write('Precision,{}'.format(','.join(map(str, pr_curve))))
