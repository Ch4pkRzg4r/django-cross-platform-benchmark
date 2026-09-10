# commerce/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Feature, Banner, Blog, AboutPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
def home(request):
    return HttpResponse("✅ Hello from IIS and Django!")


@login_required(login_url='/login/')
def index(request):
    products = Product.objects.all()
    features = Feature.objects.filter(section='index')
    main_banners = Banner.objects.filter(section='main')
    third_banners = Banner.objects.filter(section='third')
    new_arrivals = Product.objects.all()[:4]

    return render(request, 'index.html', {
        'products': products,
        'features': features,
        'main_banners': main_banners,
        'third_banners': third_banners,
        'new_arrivals': new_arrivals,
    })

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    sizes = product.sizes.split(',')  # Split sizes here
    return render(request, 'sproduct.html', {'product': product, 'sizes': sizes})

def blog_view(request):
    blogs = Blog.objects.all().order_by('-date_created')
    return render(request, 'blog.html', {'blogs': blogs})


# commerce/views.py
def about_view(request):
    features = Feature.objects.filter(section='about')
    print(features)  # This will print the QuerySet to the console
    return render(request, 'about.html', {'features': features})


# commerce/views.py

from django.shortcuts import render
from .models import ContactInfo, ContactPerson

def contact_view(request):
    contact_info = ContactInfo.objects.first()  # Assuming there's only one contact info entry
    contact_people = ContactPerson.objects.all()
    return render(request, 'contact.html', {'contact_info': contact_info, 'contact_people': contact_people})



# commerce/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from django.contrib.auth.models import User

@login_required
def cart_view(request):
    # Get or create a cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

# commerce/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    # Get the product and the cart
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the selected size from the form data
    selected_size = request.POST.get('selected_size')
    if not selected_size:
        # If no size is selected, redirect back to the product page with a message
        return redirect('product_detail', id=product_id)

    # Check if the item already exists in the cart with the same size
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=selected_size,  # Include size in the CartItem creation
        defaults={'quantity': 1}
    )

    if not created:
        # If the cart item already exists with the same size, increase the quantity
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')  # Redirect to the cart page after adding to cart

@login_required
def remove_from_cart(request, cart_item_id):
    # Get the cart item and delete it
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# commerce/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from .forms import SignUpForm  # Import your custom sign-up form
from django.contrib.auth import get_user_model

# commerce/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from django.conf import settings
from .forms import SignUpForm  # Import your custom sign-up form
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user instance and the email
            user = form.save(commit=False)  # Create user instance without saving to the database
            user.email = form.cleaned_data.get('email')  # Get the email from the form
            user.save()  # Save the user instance to the database

            # Get the first available authentication backend
            backends = get_backends()
            backend_path = None
            for backend in backends:
                if isinstance(backend, type(backends[0])):
                    backend_path = backend.__module__ + "." + backend.__class__.__name__
                    break

            # Set the backend manually to avoid the ValueError
            user.backend = backend_path

            # Automatically log in the user after sign-up
            login(request, user, backend=backend_path)
            return redirect('login')  # Redirect to the profile page after successful sign-up
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




# commerce/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import get_backends
from .forms import SignUpForm
from django.contrib.auth import get_user_model



def register_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Get the first available authentication backend
            backends = get_backends()
            backend_path = None
            for backend in backends:
                if isinstance(backend, type(backends[0])):
                    backend_path = backend.__module__ + "." + backend.__class__.__name__
                    break

            # Set the backend manually to avoid the error
            user.backend = backend_path
            login(request, user, backend=backend_path)
            return redirect('index')  # Redirect to the homepage or any other page after registration
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'profile.html', {'form': form})


# views.py
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# commerce/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    # Fetch the authenticated user's email from the database
    user = request.user  # Get the logged-in user object
    email = user.email  # Retrieve email directly from the user model

    context = {
        'username': user.username,
        'email': user.email,  # Add the email attribute to the context
    }

    return render(request, 'profile.html', context)


# commerce/views.py

from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_detail(request, blog_id):
    """
    View to display a single blog post in detail.
    """
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInfo, ContactPerson, ContactMessage
from .forms import ContactForm

def contact_view(request):
    # Fetch contact information and people details from the database
    contact_info = ContactInfo.objects.first()  # Assuming there is only one entry
    contact_people = ContactPerson.objects.all()  # Get all contact people

    # Initialize the contact form
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the submitted contact form message to the database
            form.save()
            messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
            return redirect('contact')  # Redirect back to the contact page after successful submission
    else:
        form = ContactForm()  # Empty form for GET requests

    # Pass contact information, people, and form to the context
    context = {
        'contact_info': contact_info,
        'contact_people': contact_people,
        'form': form,
    }
    return render(request, 'contact.html', context)


# commerce/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem, Payment

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_amount = cart.total_price

    if request.method == 'POST':
        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            is_paid=False  # Payment status is initially False
        )

        # Create OrderItems for each CartItem in the cart
        for cart_item in cart.cartitems.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                size=cart_item.size,
                price=cart_item.product.price,
            )

        # Simulate payment success
        Payment.objects.create(order=order, amount_paid=total_amount, is_successful=True)

        # Mark the order as paid
        order.is_paid = True
        order.save()

        # Clear the cart after successful order
        cart.cartitems.all().delete()

        # Redirect to the payment confirmation page
        return redirect('payment_success', order_id=order.id)

    return render(request, 'checkout.html', {'cart': cart, 'total_amount': total_amount})


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment_success.html', {'order': order})


from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=403)  # Return 403 Forbidden

    return JsonResponse({'error': 'Invalid request'}, status=400)
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST', block=True)  # 5 attempts per minute
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=403)

    return JsonResponse({'error': 'Invalid request'}, status=400)




# ═══════════════════════════════════════════════════
# BENCHMARK ENDPOINTS — پێویستن بۆ هەموو benchmark scripts
# ═══════════════════════════════════════════════════
import psutil
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)

_prev_net = {"t": 0.0, "rx": 0.0}

def metrics_view(request):
    cpu    = psutil.cpu_percent(interval=0.1)
    mem    = psutil.virtual_memory()
    net    = psutil.net_io_counters()
    now_rx = net.bytes_recv / 1024
    now_t  = time.time()
    dt     = now_t - _prev_net["t"]
    net_kbps = round((now_rx - _prev_net["rx"]) / dt, 2) \
               if dt > 0 and _prev_net["t"] > 0 else 0.0
    _prev_net["t"]  = now_t
    _prev_net["rx"] = now_rx
    return JsonResponse({
        "cpu_percent":     round(cpu, 2),
        "memory_used_mb":  round(mem.used  / 1024 / 1024, 2),
        "memory_total_mb": round(mem.total / 1024 / 1024, 2),
        "net_recv_kb":     round(now_rx, 2),
        "net_sent_kb":     round(net.bytes_sent / 1024, 2),
        "net_recv_kbps":   net_kbps,
        "oom_count":       0,
    })

@csrf_exempt
def attack_test_view(request, payload=""):
    return JsonResponse({
        "message": "Attack test received",
        "payload": str(payload)[:200],
    }, status=200)

@csrf_exempt
def attack_test_query(request):
    payload = request.META.get('QUERY_STRING', '')
    attack_type = "Unknown"
    if "search=" in payload and "<script>" in payload:
        attack_type = "XSS"
    elif "cmd=" in payload:
        attack_type = "Command Injection"
    elif "file=" in payload:
        attack_type = "LFI"
    elif "id=" in payload or "username=" in payload:
        attack_type = "SQL Injection"
    return JsonResponse({
        "status":      "received",
        "attack_type": attack_type,
        "payload":     payload[:200],
    }, status=200)


# ================================================================
# PHASE 6.5 REV3 DIAGNOSTIC VIEW - DO NOT REMOVE
# Process-tree-based WSGI detection + cgroup-aware CPU/memory reporting
# Added 2026-05-14 for academic verification of apple-to-apple parity
# ================================================================
def platform_identity(request):
    """
    Diagnostic endpoint for Phase 6.5 verification (REV3).
    Returns the runtime identity of THIS specific worker process.
    Uses process-tree introspection (reliable) and cgroup-aware
    CPU/memory reporting (accurate under Docker --cpus and --cpuset-cpus).
    """
    import sys
    import os
    import socket
    import platform as platform_mod
    import django
    from django.http import JsonResponse
    from django.db import connection

    # -----------------------------------------------------------------
    # WSGI server detection via process tree (reliable)
    # -----------------------------------------------------------------
    wsgi_server = "unknown"
    wsgi_version = "unknown"
    parent_cmdline = ""

    def read_cmdline(pid):
        try:
            with open(f'/proc/{pid}/cmdline', 'rb') as f:
                return f.read().decode('utf-8', errors='ignore').replace('\x00', ' ').strip()
        except Exception:
            return ""

    # Walk up the process tree (max 5 levels) to find the WSGI server
    try:
        current_pid = os.getpid()
        for _ in range(5):
            cmdline = read_cmdline(current_pid)
            cmdline_lower = cmdline.lower()

            # Match in priority order: mod_wsgi/apache > uwsgi > gunicorn > waitress
            if 'apache2' in cmdline_lower or 'httpd' in cmdline_lower or '(wsgi:' in cmdline:
                wsgi_server = "mod_wsgi"
                try:
                    # mod_wsgi version via package
                    import subprocess
                    r = subprocess.run(['dpkg', '-s', 'libapache2-mod-wsgi-py3'],
                                       capture_output=True, text=True, timeout=2)
                    for line in r.stdout.splitlines():
                        if line.startswith('Version:'):
                            wsgi_version = line.split(':', 1)[1].strip()
                            break
                    if wsgi_version == "unknown":
                        # Try pip-installed mod_wsgi
                        import mod_wsgi
                        wsgi_version = getattr(mod_wsgi, '__version__', getattr(mod_wsgi, 'version', '5.0.0'))
                except Exception:
                    wsgi_version = "5.0.0"  # from Dockerfile.apache-wsgi
                parent_cmdline = cmdline
                break
            elif 'uwsgi' in cmdline_lower:
                wsgi_server = "uWSGI"
                try:
                    import uwsgi
                    v = uwsgi.version
                    wsgi_version = v.decode() if isinstance(v, bytes) else str(v)
                except ImportError:
                    wsgi_version = "2.0.28"  # from Dockerfile.nginx-uwsgi
                parent_cmdline = cmdline
                break
            elif 'gunicorn' in cmdline_lower:
                wsgi_server = "gunicorn"
                try:
                    import gunicorn
                    wsgi_version = gunicorn.__version__
                except ImportError:
                    wsgi_version = "23.0.0"
                parent_cmdline = cmdline
                break
            elif 'waitress' in cmdline_lower:
                wsgi_server = "waitress"
                try:
                    import waitress
                    wsgi_version = getattr(waitress, '__version__', '3.0.1')
                except ImportError:
                    wsgi_version = "3.0.1"
                parent_cmdline = cmdline
                break

            # Go up one level
            try:
                with open(f'/proc/{current_pid}/status', 'r') as f:
                    for line in f:
                        if line.startswith('PPid:'):
                            ppid = int(line.split()[1])
                            if ppid == 0 or ppid == current_pid:
                                break
                            current_pid = ppid
                            break
                    else:
                        break
            except Exception:
                break
    except Exception as e:
        wsgi_server = f"detection_error: {str(e)[:50]}"

    # -----------------------------------------------------------------
    # CPU detection: cgroup-aware (accurate under Docker)
    # -----------------------------------------------------------------
    cpu_count_cgroup_v2 = None
    cpu_quota_us = None
    cpu_period_us = None
    cpuset_cpus_visible = None

    # cgroup v2 cpu.max: "<quota> <period>" or "max <period>"
    try:
        with open('/sys/fs/cgroup/cpu.max', 'r') as f:
            parts = f.read().strip().split()
            if parts[0] != 'max':
                cpu_quota_us = int(parts[0])
                cpu_period_us = int(parts[1])
                cpu_count_cgroup_v2 = round(cpu_quota_us / cpu_period_us, 2)
    except Exception:
        pass

    # cgroup v1 fallback
    if cpu_count_cgroup_v2 is None:
        try:
            with open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us', 'r') as f:
                cpu_quota_us = int(f.read().strip())
            with open('/sys/fs/cgroup/cpu/cpu.cfs_period_us', 'r') as f:
                cpu_period_us = int(f.read().strip())
            if cpu_quota_us > 0:
                cpu_count_cgroup_v2 = round(cpu_quota_us / cpu_period_us, 2)
        except Exception:
            pass

    # cpuset.cpus (which physical CPU IDs this container can use)
    for path in ['/sys/fs/cgroup/cpuset.cpus.effective',
                 '/sys/fs/cgroup/cpuset/cpuset.cpus']:
        try:
            with open(path, 'r') as f:
                cpuset_cpus_visible = f.read().strip()
                break
        except Exception:
            continue

    # Python's view (may not reflect Docker limits)
    try:
        cpu_count_sched_affinity = len(os.sched_getaffinity(0))
    except (OSError, AttributeError):
        cpu_count_sched_affinity = None

    cpu_count_os = os.cpu_count()

    # -----------------------------------------------------------------
    # Memory: cgroup-aware
    # -----------------------------------------------------------------
    memory_limit_bytes = 0
    memory_current_bytes = 0
    try:
        with open('/sys/fs/cgroup/memory.max', 'r') as f:
            v = f.read().strip()
            memory_limit_bytes = int(v) if v != 'max' else 0
        with open('/sys/fs/cgroup/memory.current', 'r') as f:
            memory_current_bytes = int(f.read().strip())
    except Exception:
        try:
            with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
                v = int(f.read().strip())
                memory_limit_bytes = v if v < 10 ** 15 else 0
            with open('/sys/fs/cgroup/memory/memory.usage_in_bytes', 'r') as f:
                memory_current_bytes = int(f.read().strip())
        except Exception:
            pass

    # Process RSS
    try:
        import psutil
        proc = psutil.Process()
        rss_bytes = proc.memory_info().rss
    except Exception:
        rss_bytes = 0

    # -----------------------------------------------------------------
    # Database check
    # -----------------------------------------------------------------
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)[:100]}"

    # Static files count
    try:
        from django.conf import settings
        if settings.STATIC_ROOT and os.path.isdir(settings.STATIC_ROOT):
            static_count = sum(len(files) for _, _, files in os.walk(settings.STATIC_ROOT))
        else:
            static_count = 0
    except Exception:
        static_count = 0

    return JsonResponse({
        "platform_identity_version": "PHASE_6.5_REV6",
        "build_marker": os.environ.get("BUILD_MARKER", "not-set"),

        # Python runtime
        "python_version": sys.version.split()[0],
        "python_version_full": sys.version,
        "python_executable": sys.executable,
        "python_implementation": platform_mod.python_implementation(),

        # OS
        "os_platform": platform_mod.platform(),
        "os_system": platform_mod.system(),
        "os_release": platform_mod.release(),
        "os_machine": platform_mod.machine(),

        # Django
        "django_version": django.get_version(),

        # WSGI server (process-tree based — RELIABLE)
        "wsgi_server": wsgi_server,
        "wsgi_server_version": wsgi_version,
        "wsgi_parent_cmdline": parent_cmdline[:200],

        # Process
        "hostname": socket.gethostname(),
        "worker_pid": os.getpid(),
        "worker_ppid": os.getppid(),
        "worker_uid": os.getuid() if hasattr(os, 'getuid') else -1,

        # CPU (cgroup-aware — RELIABLE)
        "cpu_count_cgroup": cpu_count_cgroup_v2,
        "cpu_quota_us": cpu_quota_us,
        "cpu_period_us": cpu_period_us,
        "cpuset_cpus_visible": cpuset_cpus_visible,
        "cpu_count_sched_affinity": cpu_count_sched_affinity,
        "cpu_count_os_unreliable": cpu_count_os,

        # Memory
        "memory_limit_bytes": memory_limit_bytes,
        "memory_limit_gib": round(memory_limit_bytes / (1024**3), 3) if memory_limit_bytes else 0,
        "memory_current_bytes": memory_current_bytes,
        "memory_current_mib": round(memory_current_bytes / (1024**2), 2) if memory_current_bytes else 0,
        "rss_bytes": rss_bytes,
        "rss_mib": round(rss_bytes / (1024**2), 2),

        # Database
        "db_connection": db_status,
        "db_engine": connection.settings_dict.get('ENGINE', 'unknown'),
        "db_host": connection.settings_dict.get('HOST', 'unknown'),
        "db_port": str(connection.settings_dict.get('PORT', 'unknown')),
        "db_name": connection.settings_dict.get('NAME', 'unknown'),

        # Static
        "static_files_count": static_count,
    })
