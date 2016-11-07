from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.safety import main as safety


def test_this_repo():
    safety()
