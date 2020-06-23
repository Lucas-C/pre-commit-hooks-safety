# pylint: disable=invalid-name,line-too-long
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.safety_check import main as safety


def test_dev_requirements():
    assert safety(['dev-requirements.txt', 'dev-requirements.txt']) == 0

def test_non_ok_dependency(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('urllib3==1.24.1')
    assert safety([str(requirements_file)]) == 1

def test_ignore_ok(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('urllib3==1.24.1')
    assert safety([str(requirements_file), '--ignore=37055', '--ignore=37071']) == 0

def test_editable_url_to_tarball_dependency(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-e https://files.pythonhosted.org/packages/6a/11/114c67b0e3c25c19497fde977538339530d8ffa050d6ec9349793f933faa/lockfile-0.10.2.tar.gz')
    assert safety([str(requirements_file)]) == 0

@pytest.mark.xfail(reason='cf. https://github.com/Lucas-C/pre-commit-hooks-safety/issues/1')
def test_bare_url_to_tarball_dependency(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('https://files.pythonhosted.org/packages/6a/11/114c67b0e3c25c19497fde977538339530d8ffa050d6ec9349793f933faa/lockfile-0.10.2.tar.gz')
    assert safety([str(requirements_file)]) == 0
