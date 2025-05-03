qemu-system-aarch64 \                                                                       6m 19s
  -machine virt \
  -cpu cortex-a72 \
  -m 2048 \
  -smp 2 \
  -bios /opt/homebrew/share/qemu/edk2-aarch64-code.fd \
  -nographic \
  -serial mon:stdio \
  -drive if=virtio,file=build/noble-server-cloudimg-arm64.img,format=qcow2 \
  -drive if=virtio,file=build/seed.iso,format=raw
