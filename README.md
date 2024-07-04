# AUDIO SEPARATOR
- Link: https://github.com/karaokenerds/python-audio-separator

- Queue System using celery(python) + redis + rabbitMQ

- Image information: Python 3.10


1. Clone & download model
```# command
git clone https://github.com/liemthanh-playgroundvina/audio-separator.git
cd audio-separator
```

2. Build Image
```# command
make build
```

3. Download Model
```# command
make download_model
```

4. Config
```# command
make config
... And add your config
```

5. Start
```# command
make start
```

## Pipeline
![Pipeline](https://github.com/liemthanh-playgroundvina/audio-separator/blob/main/sperate.PNG)

1. basic:
- [Beat, Vocals]
2. intermediate:
- Beat -> [Bass, Drums, Other, Vocals, Guitar, Piano]
- Vocals -> [Backing, Vocals not backing]
3. detailed
- Beat -> [Bass, Drums, Other, Vocals, Guitar, Piano]
- Vocals -> [Backing, Reverb, Delay, Clean Vocals]
4. detailed_vocals
- Beat
- Vocals -> [Backing, Reverb, Delay, Clean Vocals]