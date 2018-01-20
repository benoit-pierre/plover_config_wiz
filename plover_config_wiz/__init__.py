from pathlib import Path


RESOURCE_DIR = Path(__file__).parent / 'resources'


def resource_path(name):
    return Path(RESOURCE_DIR / name)

def resource_string(name):
    return resource_path(name).read_text(encoding='utf-8')
