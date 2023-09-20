import argparse
import json
import yaml

def read_config(config_path):

    with open(config_path, 'r') as f:
        config_data = json.load(f)

    return config_data

def generate_drone_spec(config):

    drones = []

    for i in range(config['count']):
        spec = {}
        spec['name'] = f'drone-{i+1}'
        spec['image'] = 'sred21/drone'
        spec['env'] = [{'name':key, 'value': str(val)} for key, val in config['config'].items()]

        for item in spec['env']:
            if item['name'] == 'DC_HOST':
                item['value'] = f'drone-controller-{i}'
                break

        if config['resources']:
            spec['resources'] = config['resources']

        drones.append(spec)

    return drones

def generate_dc_spec(config, drone_count):

    dcs = []

    for i in range(drone_count):
        spec = {}
        spec['name'] = f'drone-controller-{i+1}'
        spec['image'] = 'sred21/drone-controller'
        spec['env'] = [{'name':key, 'value': str(val)} for key, val in config['config'].items()]

        drone_dict = {'name': 'DRONE_HOST', 'value': f'drone-{i+1}'}
        spec['env'].append(drone_dict)

        if config['resources']:
            spec['resources'] = config['resources']

        dcs.append(spec)

    return dcs

def generate_ac_spec(config, drone_count):
     
    spec = {}
    spec['name'] = f'autonomous-controller'
    spec['image'] = 'sred21/auto-controller'

    spec['env'] = [{'name':key, 'value':str(val)} for key, val in config['config'].items()]

    dc_hosts = [f'drone-controller-{i+1}' for i in range(drone_count)]
    dc_dict = {'name': 'CONTROLLER_HOSTS', 'value': '|'.join(dc_hosts)}
    spec['env'].append(dc_dict)

    if config['resources']:
        spec['resources'] = config['resources']

    return spec

def generate_edge_spec(config):

    spec = {}
    spec['name'] = f'inference-server'
    spec['image'] = 'sred21/edge-server'
    spec['env'] = [{'name':key, 'value': str(val)} for key, val in config['config'].items()]

    if config['resources']:
        spec['resources'] = config['resources']

    return spec

def generate_pod_manifest(config_file, experiment_name, output_file_name):

    config = read_config(config_path=config_file)

    container_specs = []

    drone_specs = generate_drone_spec(config['drone'])
    dc_specs = generate_dc_spec(config['dc'], config['drone']['count'])
    ac_spec = generate_ac_spec(config['ac'], config['drone']['count'])
    edge_spec = generate_edge_spec(config['edge'])

    container_specs += drone_specs + dc_specs
    container_specs.append(ac_spec)
    container_specs.append(edge_spec)

    manifest = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': experiment_name} }
    manifest['spec'] = {'containers': container_specs}

    print(manifest)
    with open(output_file_name, 'w') as file:
        yaml.dump(manifest, file)

def generate_multipod_manifest(config_file, output_file_name):

    config = read_config(config_path=config_file)

    container_specs = []

    drone_specs = generate_drone_spec(config['drone'])
    dc_specs = generate_dc_spec(config['dc'], config['drone']['count'])
    ac_spec = generate_ac_spec(config['ac'], config['drone']['count'])
    edge_spec = generate_edge_spec(config['edge'])

    container_specs += drone_specs + dc_specs
    container_specs.append(ac_spec)
    container_specs.append(edge_spec)

    manifests = []

    for container in container_specs:
        manifest = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': container['name'], 'labels': {'name': container['name']}}}
        manifest['spec'] = {'containers': [container]}
        manifests.append(manifest)

    with open(output_file_name, 'w') as file:
        yaml.dump_all(manifests, file, default_flow_style=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a YAML manifest for Kubernetes/Docker Compose")
    parser.add_argument('exp-name')
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-c', action='store_false', dest='compose', default=False, help='Generate a docker compose YAML file')
    parser.add_argument('-t', '--type', choices=['pod', 'multipod'], dest='deployment')
    parser.add_argument('-o', '--output', required=True)
    
    args = parser.parse_args()
    
    if args.compose:
        raise NotImplementedError

    if args.deployment == 'multipod':
        generate_multipod_manifest(args.file, args.output)
        
    else:
        raise NotImplementedError
        #generate_pod_manifest(args.file, args.name, args.output)
