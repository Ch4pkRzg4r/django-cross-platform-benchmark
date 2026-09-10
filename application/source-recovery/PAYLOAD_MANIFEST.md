# Application support payload manifest

Payload carrier: `application_support_v365.b64`
Decoded gzip-tar SHA-256: `bddd760dedccabe7c13ad2454c612980e03024acb1ca838e56a0703a2aa682dd`
Source archive SHA-256: `3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`

## V2 carrier repair

On 10 September 2026 the prior GitHub text carrier was found to decode successfully only after terminal-padding normalisation, but the decoded bytes did not match the hash-locked payload identity. The mismatching hash was **not** accepted. This carrier was rebuilt from the retained source archive only after the archive itself matched the audited SHA-256 above.

The payload contains 43 reviewed UTF-8 text source files. No raw fixture, raw compose secrets, build logs or binary static/media assets are included.

| Path | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `commerce/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `commerce/admin.py` | 2419 | `f257f0b94ac1faadb1a5b49e1a81d4fda3a638fc9577d5602de6ff9cb150ced3` |
| `commerce/apps.py` | 781 | `ba2b782ba98322e8b7502a2c8ad3748a4160a9836a388f93114722889e3cb5b7` |
| `commerce/forms.py` | 2393 | `81ebf820aeed254d81df9df0fd360b0aa5bd6c60f962623b2880afeb03068c81` |
| `commerce/migrations/0001_initial.py` | 3969 | `b5ce84b30ab1e1874de673297770fedbae46928e9f6fad3e75349f92a5994ba3` |
| `commerce/migrations/0002_contactinfo_contactperson.py` | 1382 | `e499ad2ac084dd24f360122e353fb42b2b0d8d6b6667548be9cbb405fab9c9db` |
| `commerce/migrations/0003_remove_contactinfo_map_embed_url.py` | 365 | `ed53318dcd7c3b15d0197b850089d097578a9128a29b8e61d630058a1694354a` |
| `commerce/migrations/0004_cart_cartitem.py` | 1376 | `cd2dc0183f73bba51c764e346b684e151bf2bc03576c5f671023a4f7d0f82e76` |
| `commerce/migrations/0005_profile.py` | 833 | `db6fd6d9ce7d1e01e83cf51d40b7c5ebf338ff759cc526e5233eeb9aaa0e31b2` |
| `commerce/migrations/0006_profile_bio_profile_birth_date_profile_location_and_more.py` | 939 | `4b3adffa2a29d4ea9a7ef6fca2087869d1c74a51971972f486958960924ffcad` |
| `commerce/migrations/0007_customuser.py` | 2960 | `003368e83f963e1cce6e04f54e3be5d1fdabeec90f0f48370d4133016992be13` |
| `commerce/migrations/0008_delete_customuser.py` | 308 | `851e87752de578c4d7dfd03dea33f088893d6ac85668a6a405e0775579020829` |
| `commerce/migrations/0009_cartitem_size.py` | 425 | `2ed42146f9a73fdc0d192bb5418fc7b124b3a2d2d9ea870c482e431d44d450e6` |
| `commerce/migrations/0010_contactmessage.py` | 794 | `138a4b675e0bb876d2cc4a9d05cb5e8176198fcbc63f192615fcf5339818b5f1` |
| `commerce/migrations/0011_rename_date_created_contactmessage_created_at_and_more.py` | 572 | `774ca8cd27f93cdd1278ef205caf00b82baeacacb441e3b76cc4898c80d7b830` |
| `commerce/migrations/0012_alter_contactperson_image_order_payment.py` | 1945 | `0fb6be98cb63c0fc031b599ba9e4b6340fc1319424ab605291a99ba0bea644a8` |
| `commerce/migrations/0013_remove_order_cart_orderitem.py` | 1127 | `5b5a57096022e7f96e12632768f189d8e434ad5be35bd76ce5e342524eed549f` |
| `commerce/migrations/0014_order_cart_delete_orderitem.py` | 594 | `b2a048a04446f0ad2df2b9c3c6b86ded89e963f1dae8e976cdaa05cab38a36db` |
| `commerce/migrations/0015_remove_order_cart_order_status_orderitem.py` | 1289 | `9f1ebe3f6df67f95ca0fa1b80e09a33f9521af6086e5a525f256de4b43ad64e7` |
| `commerce/migrations/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `commerce/signals.py` | 671 | `79cebab56bd05ca7abff1b8585d77081cab411a79a808ad8e659befa1750d79b` |
| `commerce/templates/about.html` | 5749 | `ae5504297f029de64187b913ee1e3e6c5eef4aaf83277e34877ce965baf80d89` |
| `commerce/templates/base.html` | 2577 | `397aafed550e13d1d39a41f98bedc59804e7abd726587f415b42992abb07e7da` |
| `commerce/templates/blog.html` | 5795 | `1fc7349f7a95b2120378d1331ccbc9976b78db1995565b75813fef7e71ec5a5f` |
| `commerce/templates/blog_detail.html` | 4220 | `757c37f5307fd13402b6ea823d55d2d644956fd0377f0d01678567765e6170c1` |
| `commerce/templates/cart.html` | 6106 | `65070602b7b674afced37afac11f12aa69d08a9e95f2eb87b580673b6bb2ae10` |
| `commerce/templates/checkout.html` | 1815 | `252f4b26c8522bd30b8c4912b770c97eada84bd16734f2557567e296e44c8cd8` |
| `commerce/templates/contact.html` | 6456 | `c7bf87bcd268a2783de12e8a17ee32d203206b27b0a8457eadb2de0180d5cfb6` |
| `commerce/templates/index.html` | 8769 | `50895ca9dd29e611626dc3757ab1fca2f1ef8238f79dd2aa119628096a3b8dcc` |
| `commerce/templates/payment.html` | 165 | `cae9ee79636f76ad3bedd47fb0faa2e1f111ffbcfd194df85468913c04b10b95` |
| `commerce/templates/payment_success.html` | 1161 | `5cca813eacdd86c530a3b3b5417bc5081196aa056d8c908e0ba353feb9305b24` |
| `commerce/templates/profile.html` | 744 | `4524964f1cbe0394bab5747344e45bc4883ecc081dbfc51aeb869ae8c279b69e` |
| `commerce/templates/registration/login.html` | 1194 | `601d0497d203641f8bea224a5d8c8dde56324aac3c4007db95e5bfca1c2c5912` |
| `commerce/templates/registration/signup.html` | 1307 | `00362210b5199a59c5996b7e0ad9a70ca2668208df6f52f0d2a0f9c8ab2743f3` |
| `commerce/templates/shop.html` | 5614 | `8618948235f12a51ecd5a53df90254233f69d875897bdc85438e133dc7de5459` |
| `commerce/templates/sproduct.html` | 7367 | `a9454c9fc96093ebbdd508f9c7fe6adcddb38974b008fa78ff21ee6cd47bc9b8` |
| `commerce/templatetags/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `commerce/templatetags/custom_filters.py` | 1165 | `f8c0017b4a964307f73a26b5d36b7c03e4d6e806ce6ff36008d28b35554f2bdc` |
| `commerce/templatetags/filters.py` | 228 | `def71732ceeca19f5a3a0c22d6fe4ecfdcc877358634ab57f8c63195cb57bfd6` |
| `commerce/tests.py` | 63 | `dae0da7efdcdb3a7fb572d5e914b60631099122d4a4727ac6434c016161c5fe1` |
| `ecommerce/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `ecommerce/asgi.py` | 411 | `185bb3b77990600451c6c8cc4b39645282980639af640ace58609653f896276c` |
| `ecommerce/gunicorn_conf.py` | 357 | `5af98c90b48939ae9c4c0942f7b4040b144fadb788657a890ab920b49e28198b` |

The materializer verifies the decoded payload hash before extraction and refuses to overwrite a non-identical existing file unless explicitly requested.
