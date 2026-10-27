#!/usr/bin/env python3
"""Compute-only I-2 owner; generated from the reviewed parameter bindings."""
import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as ig
import geni.rspec.emulab

PARAMETERS = {'buildOAI': ('BOOLEAN', False),
 'buildORANSC': ('BOOLEAN', False),
 'buildOcudu': ('BOOLEAN', False),
 'buildSrsLTE': ('BOOLEAN', False),
 'buildSrsRAN4G': ('BOOLEAN', False),
 'buildSrsRANProject': ('BOOLEAN', False),
 'containerManager': ('STRING', 'docker'),
 'diskImage': ('STRING',
               'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'),
 'doLocalRegistry': ('BOOLEAN', True),
 'doNFS': ('BOOLEAN', True),
 'dockerOptions': ('STRING', ''),
 'dockerVersion': ('STRING', ''),
 'helmVersion': ('STRING', '3.18.4'),
 'installONFSDRAN': ('BOOLEAN', False),
 'installORANSC': ('BOOLEAN', True),
 'installORANSCSMO': ('BOOLEAN', False),
 'installORANSCSMOSim': ('BOOLEAN', False),
 'installOpen5GS': ('BOOLEAN', False),
 'installVNC': ('BOOLEAN', False),
 'kubeAllWorkers': ('BOOLEAN', False),
 'kubeDoMetalLB': ('BOOLEAN', False),
 'kubeEnableMultus': ('BOOLEAN', False),
 'kubeFeatureGates': ('STRING', ''),
 'kubeNetworkPlugin': ('STRING', 'calico'),
 'kubePodsSubnet': ('STRING', '10.233.0.0/16'),
 'kubeProxyMode': ('STRING', 'ipvs'),
 'kubeServiceAddresses': ('STRING', '10.96.0.0/12'),
 'kubeVersion': ('STRING', 'v1.34.3'),
 'kubeletCustomFlags': ('STRING', '[--allowed-unsafe-sysctls=net.*]'),
 'kubeletMaxPods': ('INTEGER', 120),
 'kubesprayRepo': ('STRING',
                   'https://github.com/kubernetes-sigs/kubespray.git'),
 'kubesprayUseVirtualenv': ('BOOLEAN', True),
 'kubesprayVersion': ('STRING', 'v2.30.0'),
 'linkSpeed': ('INTEGER', 0),
 'multiplexLans': ('BOOLEAN', False),
 'nfsAsync': ('BOOLEAN', False),
 'nodeCount': ('INTEGER', 3),
 'nodeType': ('NODETYPE', 'd430'),
 'ocuduRefspec': ('STRING', 'release_26_04'),
 'ocuduRepo': ('STRING', 'https://gitlab.com/ocudu/ocudu'),
 'onfRicPOWDER': ('BOOLEAN', False),
 'onfRicVersion': ('STRING', '1.4.3'),
 'oscSmoUseCachedCharts': ('BOOLEAN', True),
 'oscSmoVersion': ('STRING', 'g-release'),
 'publicIPCount': ('INTEGER', 0),
 'ricRelease': ('STRING', 'j-release'),
 'srsRANProjectRefspec': ('STRING', 'e5d5b44b92cf18d1bd1736da0148e5f9cce3721d'),
 'srsRANProjectRepo': ('STRING', 'https://github.com/srsRAN/srsRAN_Project'),
 'sslCertConfig': ('STRING', 'proxy'),
 'sslCertType': ('STRING', 'self')}
STARTUP = 'sudo /bin/bash -c \'#!/bin/bash\n# Infrastructure only; no E2 peer, recorder, subscription or security case starts here.\nset -euo pipefail\ntask_user=$(/usr/bin/geni-get user_urn 2>/dev/null | cut -d+ -f4) || task_user=$(geni-get user_urn | cut -d+ -f4)\n[[ "$task_user" =~ ^[a-zA-Z_][a-zA-Z0-9_-]*$ ]] || exit 64\n# Repository-backed POWDER profiles are checked out here before startup.\n# Preserve that checkout rather than deleting it or treating it as upstream.\nif test -e /local/repository; then\n    task_origin=$(git -C /local/repository remote get-url origin)\n    case "$task_origin" in\n        https://github.com/fkerem/fors-i2-recipient-r1|https://github.com/fkerem/fors-i2-recipient-r1.git) ;;\n        *) exit 65 ;;\n    esac\n    git -C /local/repository diff --quiet\n    test ! -e /local/i2-profile-repository\n    mv /local/repository /local/i2-profile-repository\nfi\nmkdir -p /local/setup /local/logs\nchown "$task_user" /local/setup /local/logs\ngit clone --no-checkout https://gitlab.flux.utah.edu/powder-profiles/oran.git /local/repository\ngit -C /local/repository checkout --detach e26d613e6ff69becd058b46bd55644ce18f06ca4\ngit -C /local/repository submodule update --init --recursive\npython3 - <<\'"\'"\'PY\'"\'"\'\nfrom pathlib import Path\nroot = Path(\'"\'"\'/local/repository\'"\'"\')\n# Pin deployment manifests; leave the routing/subscription implementations untouched.\npath = root/\'"\'"\'setup-oran.sh\'"\'"\'\nsource = path.read_text()\nold = \'"\'"\'git clone $RICDEPREPO -b $RICDEPBRANCH\'"\'"\'\nassert source.count(old) == 1\nsource = source.replace(old, \'"\'"\'git clone --no-checkout "$RICDEPREPO" ric-dep\\ngit -C ric-dep checkout --detach 505e5efb5f40706adccdfdc7a5289456cd01fe8a\'"\'"\')\npath.write_text(source)\n# The standard owner also starts NexRAN support services; they are unnecessary here.\npath = root/\'"\'"\'setup-driver.sh\'"\'"\'\nsource = path.read_text()\nold = \'"\'"\'setup-oran.sh setup-xapp-nexran.sh\'"\'"\'\nassert source.count(old) == 1\npath.write_text(source.replace(old, \'"\'"\'setup-oran.sh\'"\'"\'))\n# Same published OID compatibility normalization applied by the POWDER checkout service.\npath = root/\'"\'"\'test-common.py\'"\'"\'\nsource = path.read_text()\nsource = source.replace(\'"\'"\'2.25.305821105408246119474742976030998643995\'"\'"\',\n                        \'"\'"\'2.25.305821105.408246119.47474297.603099864.3995\'"\'"\')\npath.write_text(source)\nPY\nchown -R "$task_user" /local/repository\ngit -C /local/repository diff -- setup-oran.sh setup-driver.sh test-common.py > /local/setup/i2-infrastructure.patch\ntimeout --signal=TERM --kill-after=30 14400 sudo -u "$task_user" -H /bin/bash -c \\\n  \'"\'"\'/local/repository/setup-driver.sh > /local/logs/setup.log 2>&1\'"\'"\'\n\''
pc = portal.Context()
for name, (kind, default) in PARAMETERS.items():
    pc.defineParameter(name, name, getattr(portal.ParameterType, kind), default,
                       advanced=name not in ('nodeCount', 'nodeType'))
params = pc.bindParameters()
for name, (_, expected) in PARAMETERS.items():
    if getattr(params, name) != expected:
        pc.reportError(portal.ParameterError('Keep reviewed I-2 defaults unchanged.', [name]))
pc.verifyParameters()
request = pg.Request()
tour = ig.Tour()
tour.Description(ig.Tour.TEXT, 'Compute-only I-2 recipient-isolation owner. Three d430 nodes, OSC j-release RIC, no radios or UE.')
tour.Instructions(ig.Tour.MARKDOWN, 'Wait for every startup service to show Finished. No E2 peer, receiver, subscription or security case starts automatically.\nReturn the experiment status URL, UUID, all three SSH hostnames and current expiration.\nThe operator will inspect readiness, deployed image identities, dynamic RTMgr/SubMgr routes and cleanup before testing.\nKeep setup logs and generated credentials private. Stop on setup failure; do not replay startup or force completion.\nNo radio, spectrum, shared VLAN, mobile endpoint or extra public IP is requested.\n')
request.addTour(tour)
lan = pg.LAN('datalan-1')
for index in range(3):
    node = pg.RawPC('node-' + str(index))
    node.component_manager_id = 'urn:publicid:IDN+emulab.net+authority+cm'
    node.hardware_type = 'd430'
    node.disk_image = PARAMETERS['diskImage'][1]
    lan.addInterface(node.addInterface('if0'))
    node.addService(pg.Execute(shell='sh', command=STARTUP))
    node.installRootKeys(False, False)
    request.addResource(node)
request.addResource(lan)
request.addResource(ig.Password('adminPass'))
pc.printRequestRSpec(request)
