# Application support payload manifest

Payload carrier: `application_support_v365.b64`  
Decoded gzip-tar SHA-256: `7a4dacc5a01390c4b9d887d5ee5c4fb22c884d0054ab966ece5dc00a76b3ed7c`  
Source archive SHA-256: `3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`

The payload contains 43 reviewed text source files and no credentials, raw settings, raw compose secrets, build logs or binary static/media assets:

- `commerce/__init__.py`
- `commerce/admin.py`
- `commerce/apps.py`
- `commerce/forms.py`
- `commerce/migrations/0001_initial.py`
- `commerce/migrations/0002_contactinfo_contactperson.py`
- `commerce/migrations/0003_remove_contactinfo_map_embed_url.py`
- `commerce/migrations/0004_cart_cartitem.py`
- `commerce/migrations/0005_profile.py`
- `commerce/migrations/0006_profile_bio_profile_birth_date_profile_location_and_more.py`
- `commerce/migrations/0007_customuser.py`
- `commerce/migrations/0008_delete_customuser.py`
- `commerce/migrations/0009_cartitem_size.py`
- `commerce/migrations/0010_contactmessage.py`
- `commerce/migrations/0011_rename_date_created_contactmessage_created_at_and_more.py`
- `commerce/migrations/0012_alter_contactperson_image_order_payment.py`
- `commerce/migrations/0013_remove_order_cart_orderitem.py`
- `commerce/migrations/0014_order_cart_delete_orderitem.py`
- `commerce/migrations/0015_remove_order_cart_order_status_orderitem.py`
- `commerce/migrations/__init__.py`
- `commerce/signals.py`
- `commerce/templates/about.html`
- `commerce/templates/base.html`
- `commerce/templates/blog.html`
- `commerce/templates/blog_detail.html`
- `commerce/templates/cart.html`
- `commerce/templates/checkout.html`
- `commerce/templates/contact.html`
- `commerce/templates/index.html`
- `commerce/templates/payment.html`
- `commerce/templates/payment_success.html`
- `commerce/templates/profile.html`
- `commerce/templates/registration/login.html`
- `commerce/templates/registration/signup.html`
- `commerce/templates/shop.html`
- `commerce/templates/sproduct.html`
- `commerce/templatetags/__init__.py`
- `commerce/templatetags/custom_filters.py`
- `commerce/templatetags/filters.py`
- `commerce/tests.py`
- `ecommerce/__init__.py`
- `ecommerce/asgi.py`
- `ecommerce/gunicorn_conf.py`

The materializer verifies the decoded payload hash before extracting and refuses to overwrite existing files unless `--overwrite` is explicitly supplied. Local validation of this payload completed successfully with Python byte-compilation.
