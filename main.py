import json
import time
import argparse

from audio_separator.separator import Separator

# import onnxruntime
# import torch
#
# print("TORCH GPU CUDA is available: ", torch.cuda.is_available())
# print("ONNXRUNTIME TYPE: ", onnxruntime.get_device())
#
# file_path = './input/Rolling in the Deep Official Music Video.mp3'
# output_dir = f"./output/{os.path.splitext(os.path.basename(file_path))[0]}"
#
# separator = Separator(
#     model_file_dir="/models/",
#     output_dir=output_dir,
# )
#
# separator.load_model(
#     model_filename="Kim_Vocal_2.onnx", # [Beat, Vocals]
#     # model_filename="htdemucs_6s.yaml", # [Bass, Drums, Other, Vocals, Guitar, Piano]
#     # model_filename="UVR_MDXNET_KARA.onnx", # [Backing, Vocals not backing]
#     # model_filename="Reverb_HQ_By_FoxJoy.onnx", # [Vocals not reverb, Reverb] ->
#     # model_filename="UVR-De-Echo-Aggressive.pth", # [Vocals not Delay, Delay]
#     # model_filename="UVR-DeNoise.pth", [_, Clean Vocals]


def separate_basic(file_path):
    """[Beat, Vocals]"""
    start_time = time.time()
    output_dir = f"./output/{int(start_time)}"

    separator = Separator(
        model_file_dir="/models/",
        output_dir=output_dir,
    )
    separator.load_model(
        model_filename="Kim_Vocal_2.onnx",
    )
    beat, raw_vocals = separator.separate(file_path)

    instrumental = {"beat": output_dir + "/" + beat}
    vocals = {"raw_vocals": output_dir + "/" + raw_vocals}
    output = {
        "instrumental": instrumental,
        "vocals": vocals
    }

    return {"output_dir": output_dir, "output": output}

def separate_intermediate(file_path):
    """
    [Beat, Vocals]
    Beat -> [Bass, Drums, Other, Vocals, Guitar, Piano]
    Vocals -> [Backing, Vocals not backing]
    """
    start_time = time.time()
    output_dir = f"./output/{int(start_time)}"

    separator = Separator(
        model_file_dir="/models/",
        output_dir=output_dir,
    )
    # Phase 1
    separator.load_model(
        model_filename="Kim_Vocal_2.onnx",
    )
    beat, raw_vocals = separator.separate(file_path)
    # Phase 2
    separator.load_model(
        model_filename="htdemucs_6s.yaml",
    )
    bass, drums, other, _, guitar, piano = separator.separate(output_dir + "/" + beat)
    # Phase 3
    separator.load_model(
        model_filename="UVR_MDXNET_KARA.onnx",
    )
    backing, vocals_not_backing = separator.separate(output_dir + "/" + raw_vocals)
    instrumental = {
        "beat": output_dir + "/" + beat,
        "bass": output_dir + "/" + bass,
        "drums": output_dir + "/" + drums,
        "other": output_dir + "/" + other,
        "guitar": output_dir + "/" + guitar,
        "piano": output_dir + "/" + piano,
    }
    vocals = {
        "raw_vocals": output_dir + "/" + raw_vocals,
        "backing": output_dir + "/" + backing,
        "clean_vocals": output_dir + "/" + vocals_not_backing,
    }
    output = {
        "instrumental": instrumental,
        "vocals": vocals
    }
    return {"output_dir": output_dir, "output": output}


def separate_detailed(file_path):
    """
    [Beat, Vocals]
    Beat -> [Bass, Drums, Other, Vocals, Guitar, Piano]
    Vocals -> [Backing, Reverb, Delay, Clean Vocals]
    """
    start_time = time.time()
    output_dir = f"./output/{int(start_time)}"

    separator = Separator(
        model_file_dir="/models/",
        output_dir=output_dir,
    )
    # Phase 1
    separator.load_model(
        model_filename="Kim_Vocal_2.onnx",
    )
    beat, raw_vocals = separator.separate(file_path)
    # Phase 2
    separator.load_model(
        model_filename="htdemucs_6s.yaml",
    )
    bass, drums, other, _, guitar, piano = separator.separate(output_dir + "/" + beat)
    # Phase 3
    separator.load_model(
        model_filename="UVR_MDXNET_KARA.onnx",
    )
    backing, vocals_not_backing = separator.separate(output_dir + "/" + raw_vocals)
    # Phase 4
    separator.load_model(
        model_filename="Reverb_HQ_By_FoxJoy.onnx",
    )
    vocals_not_reverb, reverb = separator.separate(output_dir + "/" + vocals_not_backing)
    # Phase 5
    separator.load_model(
        model_filename="UVR-De-Echo-Aggressive.pth",
    )
    vocals_not_delay, delay = separator.separate(output_dir + "/" + vocals_not_reverb)
    # Phase 6
    separator.load_model(
        model_filename="UVR-DeNoise.pth",
    )
    _, clean_vocals = separator.separate(output_dir + "/" + vocals_not_delay)

    instrumental = {
        "beat": output_dir + "/" + beat,
        "bass": output_dir + "/" + bass,
        "drums": output_dir + "/" + drums,
        "other": output_dir + "/" + other,
        "guitar": output_dir + "/" + guitar,
        "piano": output_dir + "/" + piano,
    }

    vocals = {
        "raw_vocals": output_dir + "/" + raw_vocals,
        "backing": output_dir + "/" + backing,
        "reverb": output_dir + "/" + reverb,
        "delay": output_dir + "/" + delay,
        "clean_vocals": output_dir + "/" + clean_vocals,
    }
    output = {
        "instrumental": instrumental,
        "vocals": vocals
    }
    return {"output_dir": output_dir, "output": output}


# print(separate_basic(path)) # 20s
# print(separate_intermediate(path)) # 40s
# print(separate_detailed(path)) # 90s

def main():
    parser = argparse.ArgumentParser(description="Separate-Audio")
    parser.add_argument('path', type=str, help='Path to be passed to the function')
    parser.add_argument('level', type=str, choices=['basic', 'intermediate', 'detailed'], help='Level of separation')

    args = parser.parse_args()
    start_time = time.time()

    if args.level == 'basic':
        result = separate_basic(args.path)
    elif args.level == 'intermediate':
        result = separate_intermediate(args.path)
    elif args.level == 'detailed':
        result = separate_detailed(args.path)
    else:
        raise ValueError(f"Dont support '{args.level}' level")

    result['execution_time'] = time.time() - start_time

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
