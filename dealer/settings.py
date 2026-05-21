from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ✅ CHANGE 1: Replace ALLOWED_HOSTS = ['*'] with your real domain
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
import os
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dealer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dealer.wsgi.application'

DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================
# ✅ CHANGE 2: HTTPS & SECURITY SETTINGS
# These only activate when DEBUG=False (i.e. in production)
# ==============================================================
if not DEBUG:
    # Force all HTTP traffic to redirect to HTTPS
    SECURE_SSL_REDIRECT = True

    # Browsers must use HTTPS for 1 year (31536000 seconds)
    SECURE_HSTS_SECONDS = 31536000

    # Apply HSTS to all subdomains (e.g. www.autoprimemotors.ng)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Allow site to be submitted to browser HSTS preload lists
    SECURE_HSTS_PRELOAD = True

    # Session cookie only sent over HTTPS — protects logged-in admin session
    SESSION_COOKIE_SECURE = True

    # CSRF cookie only sent over HTTPS — protects your inquiry & quote forms
    CSRF_COOKIE_SECURE = True

    # Prevent browsers from guessing/sniffing content types
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Prevent AutoPrime from being embedded in iframes on other sites (clickjacking)
    X_FRAME_OPTIONS = 'DENY'

    # Tell browser to block detected XSS attacks
    SECURE_BROWSER_XSS_FILTER = True

    # Use the proxy's HTTPS header (needed on Render, Railway, Heroku etc.)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Add this near the bottom
if not DEBUG:
    # This helps Whitenoise create unique file names when content changes
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # ==================== CACHE & STATIC ====================
    if not DEBUG:
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

        # Disable caching for HTML
        SESSION_COOKIE_AGE = 0
        CSRF_COOKIE_MAX_AGE = 0