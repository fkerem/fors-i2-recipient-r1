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
STARTUP = 'sudo -n /bin/bash /local/repository/bootstrap.sh'
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
