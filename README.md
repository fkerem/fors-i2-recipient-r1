# I-2 recipient isolation on POWDER

Compute-only preparation for a bounded recipient-isolation assessment: three d430 nodes, Ubuntu 22.04, and the OSC j-release RIC. No radio, spectrum, UE, Open5GS, SMO, VNC, shared VLAN or extra public IP is requested.

## Import and initiate manually

1. In POWDER, create a repository-backed profile in project **oransec** using `https://github.com/fkerem/fors-i2-recipient-r1.git`.
2. Select tag **profile-r1** and keep all reviewed parameter defaults unchanged.
3. Instantiate **i2-recipient-r1** and request 48 hours, subject to current admission and lease availability.
4. Wait for all three startup services to show **Finished**. Return the status URL, UUID, three SSH hosts and current displayed expiration to the operator.

Only infrastructure starts automatically. OCUDU, test receivers, subscriptions and security cases remain separate. Native dependency compatibility, deployed image identities, readiness and cleanup must be qualified before testing. A rendered profile is not a completed native installation.

Startup preserves POWDER's profile checkout at `/local/i2-profile-repository` and downloads the official infrastructure source into `/local/repository`. Infrastructure derives from `powder-profiles/oran` commit `e26d613e6ff69becd058b46bd55644ce18f06ca4`; ric-dep is pinned to `505e5efb5f40706adccdfdc7a5289456cd01fe8a`. The wrapper skips unrelated NexRAN setup and applies the published OID compatibility normalization. It does not change routing/subscription logic. Some upstream helper downloads and image tags remain mutable; record actual versions and digests before cases.

Stop on an admission or startup failure and return the exact error; do not replay infrastructure setup or force completion. Keep setup logs, generated passwords and Kubernetes credentials private. This repository contains only the profile, these instructions and its license.

The profile wrapper is MIT licensed. Downloaded upstream software retains its own licenses. No vulnerability result or universal isolation claim is made by this profile.
