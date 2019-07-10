#!/bin/bash
METHOD=$(echo $1 | awk '{print tolower($0)}')
FEATURES=$(echo $2 | awk '{print tolower($0)}')

if [[ $METHOD != "custom" ]]; then
    echo "Note: the available methods are GV, BOW, LBOW, DML, HC"
    if [[ $METHOD == "gv"  ||  $METHOD == "bow"  ||  $METHOD == "dml" ]]; then
        echo "Selected method: $1"
        echo "Available features: VGG, RESNET, INCEPTION, C3D_FC, C3D_INT, I3D_FC, I3D_INT"
    elif [[ $METHOD == "hc" ]]; then
        echo "Selected method: $1"
        echo "Available features: CNN, 3DCNN"
    elif [[ $METHOD == "lbow" ]]; then
        echo "Selected method: $1"
        echo "Available features: VGG, RESNET, INCEPTION, C3D_INT, I3D_INT"
    else
        echo "Error: method does not exists. Please, select one of the available methods"
        exit
    fi

    mkdir -p ./runs/$METHOD
    if [[ $METHOD == *"bow"* ]]; then
        EXT="mtx"
    else
        EXT="npy"
    fi
    
    if [[ $METHOD == *"hc"* ]]; then
        SIMILARITY="hamming"
    else
        SIMILARITY="cosine"
    fi

    URL=http://ndd.iti.gr/features/$METHOD/$FEATURES.$EXT
    FEATURE_FILE=./runs/$METHOD/$FEATURES.$EXT
    RESULT_FILE=./results/${METHOD}_${FEATURES}.json
    
    wget -c -N $URL -O $FEATURE_FILE    
else
    FEATURE_FILE=$2
    RESULT_FILE=./results/custom_run.json
    if [[ ${FEATURE_FILE: -4} != ".npy" &&  ${FEATURE_FILE: -4} != ".mtx" ]]; then
        echo "Error: format of the provided file is not supported. Please, provide an .npy or .mtx file"
        exit
    fi
    SIMILARITY="cosine"
fi

mkdir -p ./results
python calculate_similarities.py --feature_file $FEATURE_FILE --result_file $RESULT_FILE --similarity_metric $SIMILARITY


printf "\n\nEvaluation on DSVR task\n-----------------------\n"
EXPORT_FILE=./results/dsvr_${METHOD}_${FEATURES}.csv
python evaluation.py --result_file $RESULT_FILE --relevant_labels ND,DS --export_file $EXPORT_FILE --save_results --quiet

printf "\n\nEvaluation on CSVR task\n-----------------------\n"
EXPORT_FILE=./results/csvr_${METHOD}_${FEATURES}.csv
python evaluation.py --result_file $RESULT_FILE --relevant_labels ND,DS,CS --export_file $EXPORT_FILE --save_results --quiet

printf "\n\nEvaluation on ISVR task\n-----------------------\n"
EXPORT_FILE=./results/isvr_${METHOD}_${FEATURES}.csv
python evaluation.py --result_file $RESULT_FILE --relevant_labels ND,DS,CS,IS --export_file $EXPORT_FILE --save_results --quiet
