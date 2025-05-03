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
