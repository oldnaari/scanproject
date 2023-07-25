### scanproject

This is a tool that can help you scan projects to find code segments that are responsible for different things.


## Installation

```shell
pip install git+ssh://git@gitlab.com/daniil.hayrapetyan/scanproject.git
```

After installing with pip please provide the API key as 
```shell
scanproject activate --api-key <your-api-key>
```

By default, this tools uses `gpt-3.5-turbo` you can switch to gpt-4 with command

```shell
scanproject activate --model gpt-4
```

## Examples

For example if you want to find files that contain installation 
instructions you can use command

```shell
$ snapproject find "contains installation requirements"

requirements.txt
setup.py
.idea/inspectionProfiles/Project_Default.xml
src/scanproject.egg-info/requires.txt
```

## Building Detailed Reports
You can also use the `--report [-r]` flag to generate a full report with detailed motivations behind each decision.
The output
