#!/usr/bin/python
# Copyright (c) 2019, Oracle and/or its affiliates.
# This software is made available to you under the terms of the GPL 3.0 license or the Apache 2.0 license.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Apache License v2.0
# See LICENSE.TXT for details.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: oci_virtual_circuit_bandwidth_shape_facts
short_description: Fetches details of one or more OCI virtual circuit bandwidth shapes
description:
     - Fetches details of the OCI virtual circuit bandwidth shapes
version_added: "2.5"
options:
    compartment_id:
        description: Identifier of the compartment under which virtual circuit bandwidth shapes exists
        required: true
author:
    - "Debayan Gupta(@debayan_gupta)"
extends_documentation_fragment: [ oracle ]
"""

EXAMPLES = """
# Note: These examples do not set authentication details.
# Fetch All virtual circuit bandwidth shapes under a specific compartment
- name: FFetch All virtual circuit bandwidth shapes under a specific compartment
  oci_virtual_circuit_bandwidth_shape_facts:
      compartment_id: 'ocid1.compartment.oc1.iad.xxxxxEXAMPLExxxxx'
"""

RETURN = """
    oci_virtual_circuit_bandwidth_shapes:
        description: Attributes of the virtual circuit bandwidth shapes.
        returned: success
        type: complex
        contains:
            name:
                description: The name of the bandwidth shape.
                returned: always
                type: string
                sample: 10 Gbps
            bandwidth_in_mbps:
                description: The bandwidth in Mbps.
                returned: always
                type: int
                sample: 10
        sample: [{
                    "name": "1 Gbps",
                    "bandwidth_in_mbps": 1000
                }]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oracle import oci_utils


try:
    from oci.core import VirtualNetworkClient
    from oci.exceptions import ServiceError
    from oci.util import to_dict

    HAS_OCI_PY_SDK = True
except ImportError:
    HAS_OCI_PY_SDK = False

logger = None


def list_virtual_circuit_bandwidth_shapes(virtual_network_client, module):
    result = dict(virtual_circuit_bandwidth_shapes="")
    compartment_id = module.params.get("compartment_id")
    get_logger().info(
        "Retrieving all virtual circuit Bandwidth Shapes in Compartment %s",
        compartment_id,
    )
    try:
        result["virtual_circuit_bandwidth_shapes"] = to_dict(
            oci_utils.list_all_resources(
                virtual_network_client.list_virtual_circuit_bandwidth_shapes,
                compartment_id=compartment_id,
            )
        )
    except ServiceError as ex:
        get_logger().error(
            "Unable to list all virtual circuit Bandwidth Shapes due to: %s", ex.message
        )
        module.fail_json(msg=ex.message)

    return result


def set_logger(input_logger):
    global logger
    logger = input_logger


def get_logger():
    return logger


def main():
    logger = oci_utils.get_logger("oci_virtual_circuit_bandwidth_shape_facts")
    set_logger(logger)
    module_args = oci_utils.get_common_arg_spec()
    module_args.update(dict(compartment_id=dict(type="str", required=True)))
    module = AnsibleModule(argument_spec=module_args)

    if not HAS_OCI_PY_SDK:
        module.fail_json(msg="oci python sdk required for this module")
    virtual_network_client = oci_utils.create_service_client(
        module, VirtualNetworkClient
    )

    result = list_virtual_circuit_bandwidth_shapes(virtual_network_client, module)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
