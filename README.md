# Tools for subtitles

A few tools that do things that I needed doing on subtitles. The star of the show is OpenAI's whisper model,
used to generate a subtitle that not only is correct, but adheres to the constraints that make up a good subtitle
(characters per second limit, minimal distance between cues else they are concatenated...)

## Preview

`uv run .\auto-sub\auto-sub.py susd_dnd.acc base.en`

| Before                                | After                                 |
| ------------------------------------- | ------------------------------------- |
| ![](./readme-images/mpv-shot0005.jpg) | ![](./readme-images/mpv-shot0001.jpg) |
| ![](./readme-images/mpv-shot0006.jpg) | ![](./readme-images/mpv-shot0002.jpg) |
| ![](./readme-images/mpv-shot0007.jpg) | ![](./readme-images/mpv-shot0004.jpg) |