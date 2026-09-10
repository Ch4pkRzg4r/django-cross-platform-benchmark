#!/usr/bin/env python3
"""Load the privacy-safe reproducibility fixture.

This loader is intentionally separate from the retained historical `load_data.py`.
It defaults to `datadump.PUBLIC.json`, disables the known profile-creation
signals during `loaddata`, and never embeds a benchmark credential.
"""

from __future__ import annotations

import os
from pathlib import Path

# Prevent CommerceConfig.ready() from importing the secondary signal handlers.
os.environ.setdefault("LOADING_FIXTURES", "true")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save

# models.py contains a historical receiver registered at model import time.
try:
    from commerce.models import create_or_update_user_profile

    post_save.disconnect(create_or_update_user_profile, sender=User)
except (ImportError, AttributeError):
    pass

# Defensive disconnect in case the separate signals module has already been imported.
try:
    from commerce.signals import create_user_profile, save_user_profile

    post_save.disconnect(create_user_profile, sender=User)
    post_save.disconnect(save_user_profile, sender=User)
except (ImportError, AttributeError):
    pass

HERE = Path(__file__).resolve().parent
fixture = Path(os.environ.get("FIXTURE_PATH", HERE / "datadump.PUBLIC.json"))
if not fixture.is_file():
    raise FileNotFoundError(f"Fixture not found: {fixture}")

# `flush` is opt-in because it is destructive. Use only on a disposable/reproduction DB.
if os.environ.get("RESET_BEFORE_FIXTURE_LOAD", "false").lower() == "true":
    call_command("flush", interactive=False)

call_command("loaddata", str(fixture), verbosity=1)
print(f"PASS: loaded privacy-safe fixture {fixture}")
