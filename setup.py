import json
import os

if __name__ == '__main__':

    instance_info_fpath = os.environ['AWSPOT_RESOURCES_FILE']

    with open(instance_info_fpath, 'w') as f:
        resources = {'ec2': {'active': {},
                             'terminated': {}},
                     'fleet': {'active': {},
                               'terminated': {}}

        f.write(json.dumps(resources))
