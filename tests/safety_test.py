from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.safety import main as safety


def test_dev_requirements():
    assert safety(['dev-requirements.txt', 'dev-requirements.txt']) == 0

def test_non_ok_dependency(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('urllib3==1.18')
    assert safety([str(requirements_file)]) == 1
