# Static asset boundary

The retained application static tree contains 73 files (17,063,611 bytes). Every file has been SHA-256 inventoried in `documentation/STATIC_ASSET_MANIFEST_V365.csv`; the complete tree passed the repository secret-pattern gate.

These assets are useful for reconstructing the historical visual application, but they are **not required for the measured k6 GET workload**: k6 requested the Django routes directly and did not behave as a browser fetching referenced CSS/images/fonts/video after each HTML response.

The static set includes third-party-looking fonts, images and a video. Presence in the private research repository does not constitute a claim that all such assets are author-owned or relicensed under MIT/CC BY. See `LICENSING.md`.

If the repository is made public before asset provenance is fully resolved, the safest release is to retain the SHA-256 manifest and omit/replace uncertain binary assets. This does not change the frozen 280×39 dataset, the measured server responses, or the thesis inferential results.
