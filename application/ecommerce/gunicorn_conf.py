# ================================================================
# Gunicorn Configuration
# ================================================================
# Remove "Server: gunicorn" header for proxy compatibility
# ================================================================

import gunicorn

# سڕینەوەی server header
gunicorn.SERVER = ''
