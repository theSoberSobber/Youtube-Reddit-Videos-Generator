# Reddit Video Generator
You need a UNIX Sytem for this to work, absolutely no Windows Support is Provided, however if you're willing to jump some hoops, WSL can work just fine.

- You need to build and use the `main` binary from whisper.cpp, one is provided but it's bad practice to use random binaries from the internet, so do whatever you please.
- Needs ffmpeg, libmagickc++-dev (devel not pip)
- Python deps:
	- moviepy
	- pytube
- Or just use the workflow as a build/usage guide

# Automatic Setup (Ubuntu Only)
- `sudo apt update && sudo apt upgrade && sudo apt install git`
- `git clone --recursive git@github.com:theSoberSobber/Youtube-Reddit-Videos-Generator.git`
- `chmod +x setup_ubuntu.sh`
- `sudo ./setup_ubuntu.sh --verbose` (verbose is optional)

# Assets
- The Video and the font (Courier New or Mutant BB) all belong to their respective owners and I claim no ownership over them.
- You can find more assets to use [here](https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/background_videos.json)
