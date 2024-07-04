import subprocess
import json


def separate_audio(file_path, level):
    """
    level: ['basic', 'intermediate', 'detailed']

        {
          "output_dir": "./output/1719996384",
          "output": {
              "instrumental": {
                "beat": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2.wav",
                "bass": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2_(Bass)_htdemucs_6s.wav",
                "drums": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2_(Drums)_htdemucs_6s.wav",
                "other": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2_(Other)_htdemucs_6s.wav",
                "guitar": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2_(Guitar)_htdemucs_6s.wav",
                "piano": "./output/1719997975/Anh Sẽ_320kbps_(Instrumental)_Kim_Vocal_2_(Piano)_htdemucs_6s.wav"
              },
              "vocals": {
                "raw_vocals": "./output/1719997975/Anh Sẽ_320kbps_(Vocals)_Kim_Vocal_2.wav",
                "backing": "./output/1719997975/Anh Sẽ_320kbps_(Vocals)_Kim_Vocal_2_(Instrumental)_UVR_MDXNET_KARA.wav",
                "reverb": "./output/1719997975/Anh Sẽ_320kbps_(Vocals)_Kim_Vocal_2_(Vocals)_UVR_MDXNET_KARA_(Reverb)_Reverb_HQ_By_FoxJoy.wav",
                "delay": "./output/1719997975/Anh Sẽ_320kbps_(Vocals)_Kim_Vocal_2_(Vocals)_UVR_MDXNET_KARA_(Instrumental)_Reverb_HQ_By_FoxJoy_(Instrumental)_UVR-De-Echo-Aggressive.wav",
                "clean_vocals": "./output/1719997975/Anh Sẽ_320kbps_(Vocals)_Kim_Vocal_2_(Vocals)_UVR_MDXNET_KARA_(Instrumental)_Reverb_HQ_By_FoxJoy_(No Echo)_UVR-De-Echo-Aggressive_(Instrumental)_UVR-DeNoise.wav"
              }
            },
          "execution_time": 16
        }

    """
    args = ["python", "main.py", file_path, level]
    print(args)
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    output = result.stdout.strip()
    output = json.loads(output, strict=False)

    return output['output_dir'], output['output'], output['execution_time']
