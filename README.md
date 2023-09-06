# prowess-dronesim

A simple framework to simulate drone workloads on the PROWESS testbed.

![overview](assets/img/overview.png)

## Containers

Containers required for the experiment are uploaded to hub.docker.com (user: sred21) and their source files are also available in this repository:

1. drone
2. drone-controller
3. auto-controller
4. edge-server


## Experimentation

![generator-script](assets/img/manifest_generation.png)

```bash

# install pyYAML package
pip install -r requirements.txt

# Run the manifest generation script

python k8s_generator.py arg1 arg2 arg3

```

Scripts arguments:
1. Path to the experiment configuration file (JSON)
2. Name of the experiment
3. Path to file where output YAML manifest is stored (YAML)

Example:

```bash

python k8s_generator.py experiment_config.json experiment-1 experiment-1.yaml

```
