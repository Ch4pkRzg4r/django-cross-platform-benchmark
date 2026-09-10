# Fly.io public-derivative provenance

Raw retained source path on the user workstation:

`C:\Users\Tech Line\fly-deploy\fly.toml`

Raw source SHA-256:

`7760d48f66c207e73d9a2e41fe6df0dbe80968b736cd148119719517bd18f300`

The source hash matched the prior local inventory before derivation. The raw file was **not** promoted because it contained credential-bearing assignments. The supplied intermediate public derivative had SHA-256 `b3eda51b071d90b4652b40f9812ac4440bcb699c82efb990ff0896bc5f229ac6`; repository promotion applied one additional safety step by redacting the public app name and database endpoint as well.

Preserved deployment semantics include Frankfurt primary region, image identity, immediate deploy strategy, internal port 8000, health check path, scale-to-zero-related machine settings, and the 2-vCPU/2048-MB shared machine profile represented by the retained file.

This is a sanitised configuration derivative, not a claim that every provider-internal setting or historical control-plane state can be reconstructed.
