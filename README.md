# Setup ISO with Cloud Init

## Generate Cloud Init files

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate.py
```

## Build seed.iso file

```shell
xorriso -as mkisofs -output build/seed.iso -volid cidata -joliet -rock build/user-data build/meta-data
```

## Run VM on Apple Silicon with QEMU

```shell
$ brew install qemu

$ qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a72 \
  -m 2048 \
  -smp 2 \
  -bios /opt/homebrew/share/qemu/edk2-aarch64-code.fd \
  -nographic \
  -serial mon:stdio \
  -drive if=virtio,file=build/noble-server-cloudimg-arm64.img,format=qcow2 \
  -drive if=virtio,file=build/seed.iso,format=raw
```
