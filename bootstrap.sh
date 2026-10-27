#!/bin/bash
# Infrastructure only; no E2 peer, recorder, subscription or security case starts here.
set -euo pipefail
umask 077
test ! -e /local/setup
test ! -e /local/i2-profile-repository
test ! -e /etc/kubernetes/admin.conf
task_user=$(/usr/bin/geni-get user_urn 2>/dev/null | cut -d+ -f4) || task_user=$(geni-get user_urn | cut -d+ -f4)
[[ "$task_user" =~ ^[a-zA-Z_][a-zA-Z0-9_-]*$ ]] || exit 64
# Repository-backed POWDER profiles are checked out here before startup.
# Preserve that checkout rather than deleting it or treating it as upstream.
if test -e /local/repository; then
    task_origin=$(git -C /local/repository remote get-url origin)
    case "$task_origin" in
        https://github.com/fkerem/fors-i2-recipient-r1|https://github.com/fkerem/fors-i2-recipient-r1.git) ;;
        *) exit 65 ;;
    esac
    test -z "$(git -C /local/repository status --porcelain)"
    test ! -e /local/i2-profile-repository
    mv /local/repository /local/i2-profile-repository
fi
mkdir -p /local/setup /local/logs
chown "$task_user" /local/setup /local/logs
git clone --no-checkout https://gitlab.flux.utah.edu/powder-profiles/oran.git /local/repository
git -C /local/repository checkout --detach e26d613e6ff69becd058b46bd55644ce18f06ca4
git -C /local/repository submodule update --init --recursive
python3 - <<'PY'
from pathlib import Path
root = Path('/local/repository')
# Pin deployment manifests; leave the routing/subscription implementations untouched.
path = root/'setup-oran.sh'
source = path.read_text()
old = 'git clone $RICDEPREPO -b $RICDEPBRANCH'
assert source.count(old) == 1
source = source.replace(old, 'git clone --no-checkout "$RICDEPREPO" ric-dep\ngit -C ric-dep checkout --detach 505e5efb5f40706adccdfdc7a5289456cd01fe8a')
path.write_text(source)
# The standard owner also starts NexRAN support services; they are unnecessary here.
path = root/'setup-driver.sh'
source = path.read_text()
old = 'setup-oran.sh setup-xapp-nexran.sh'
assert source.count(old) == 1
path.write_text(source.replace(old, 'setup-oran.sh'))
# This assessment keeps completion receipts private; do not send upstream email.
source = path.read_text()
old = 'HEADNODESCRIPTS="${HEADNODESCRIPTS} setup-end.sh"'
assert source.count(old) == 1
path.write_text(source.replace(old, '# Completion is recorded privately by the bounded assessment wrapper.'))
# The Kubernetes installer has a separate progress-email hook.
path = root/'setup-kubespray.sh'
source = path.read_text()
old = ('echo "Your ${EXPTTYPE} instance is setting up on $NFQDN ." '
       + chr(92) + chr(10)
       + '    |  mail -s "${EXPTTYPE} Instance Setting Up" ${SWAPPER_EMAIL} &')
assert source.count(old) == 1
source = source.replace(old, '# Progress is recorded privately; no setup email.')
# Kubespray 2.30 checksum keys and its Ansible version filter omit the v prefix.
old = 'kube_version: ${KUBEVERSION}'
assert source.count(old) == 1
path.write_text(source.replace(old, 'kube_version: ${KUBEVERSION#v}'))
# Same published OID compatibility normalization applied by the POWDER checkout service.
path = root/'test-common.py'
source = path.read_text()
source = source.replace('2.25.305821105408246119474742976030998643995',
                        '2.25.305821105.408246119.47474297.603099864.3995')
path.write_text(source)
PY
chown -R "$task_user" /local/repository
git -C /local/repository diff -- setup-oran.sh setup-driver.sh setup-kubespray.sh test-common.py > /local/setup/i2-infrastructure.patch
timeout --signal=TERM --kill-after=30 14400 sudo -u "$task_user" -H /bin/bash -c \
  '/local/repository/setup-driver.sh > /local/logs/setup.log 2>&1'
