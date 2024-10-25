testing_dir="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/camera_ready/testing"

# List the contents of the directory
big_sequences=$(ls "$testing_dir")

# Loop through the contents and print each entry
for big_sequence in $big_sequences; do
    # echo "$big_sequences"
    sequences=$(ls "$testing_dir/$big_sequence")

    for sequence in $sequences; do
        # echo "$testing_dir/$big_sequence/$sequence"
        # image_path="$testing_dir/$big_sequence/$sequence/exo/cam01/images"
        # output_path="romp_inference/$big_sequence/$sequence/exo/cam01/images"
        CUDA_VISIBLE_DEVICES=0 python convert_result.py --big_sequence $big_sequence --sequence $sequence
    done
done
    # parser.add_argument('--big_sequence', type=str, default='13_hugging')
    # parser.add_argument('--sequence', type=str, default='002_hugging')
    # parser.add_argument('--cam', type=str, default='cam01')
# Add key-value pairs to the dictionary


# romp --mode=video --calc_smpl --render_mesh -i=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/camera_ready/testing/13_hugging/002_hugging/exo/cam01/images \\
#     -o=romp_inference/13_hugging/002_hugging/exo/cam01/images