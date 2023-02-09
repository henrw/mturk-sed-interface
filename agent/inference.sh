CHECKPOINT_PATH="Cnn14_DecisionLevelMax_mAP=0.385.pth"
MODEL_TYPE="Cnn14_DecisionLevelMax"
CUDA_VISIBLE_DEVICES=0 python3 pytorch/inference.py sound_event_detection \
    --model_type=$MODEL_TYPE \
    --checkpoint_path=$CHECKPOINT_PATH \
    --audio_path="../data/sound0.wav"