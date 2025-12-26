[app]

# ═══════════════════════════════════════════════════════════
#           APP BASIC INFORMATION
# ═══════════════════════════════════════════════════════════

# App ka title (phone pe dikhega)
title = SMS Forwarder

# Package name (unique identifier)
package.name = smsforwarder
package.domain = org.example

# Source code ka location
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# App version (update karne pe badha sakte ho)
version = 1.0

# ═══════════════════════════════════════════════════════════
#           PYTHON REQUIREMENTS
# ═══════════════════════════════════════════════════════════

# Python packages jo chahiye (comma-separated, no spaces!)
requirements = python3,kivy,pyjnius,requests,android

# ═══════════════════════════════════════════════════════════
#           ANDROID PERMISSIONS
# ═══════════════════════════════════════════════════════════

# SMS, Contacts, Internet, Phone State permissions
# Android 15 compatible permissions
permissions = READ_SMS,RECEIVE_SMS,SEND_SMS,INTERNET,READ_CONTACTS,READ_PHONE_STATE,POST_NOTIFICATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_DATA_SYNC
android.permissions = READ_SMS,RECEIVE_SMS,SEND_SMS,INTERNET,READ_CONTACTS,READ_PHONE_STATE,POST_NOTIFICATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_DATA_SYNC

# Android 15 specific: Foreground service type
android.manifest.service_attributes = android:foregroundServiceType="dataSync"

# ═══════════════════════════════════════════════════════════
#           ANDROID VERSION SETTINGS
# ═══════════════════════════════════════════════════════════

# Target Android API (35 = Android 15) - Latest!
android.api = 35

# Minimum Android version (21 = Android 5.0 Lollipop)
android.minapi = 21

# NDK version (latest stable)
android.ndk = 26b

# SDK version (matches API level)
android.sdk = 35

# Compile SDK version
android.compile_sdk = 35

# ═══════════════════════════════════════════════════════════
#           APP APPEARANCE
# ═══════════════════════════════════════════════════════════

# App icon (optional - agar custom icon chahiye)
# icon.filename = %(source.dir)s/icon.png

# Loading screen (optional)
# presplash.filename = %(source.dir)s/presplash.png

# Screen orientation (portrait/landscape/all)
orientation = portrait

# App theme (no title bar)
android.theme = @android:style/Theme.NoTitleBar

# ═══════════════════════════════════════════════════════════
#           BACKGROUND SERVICE
# ═══════════════════════════════════════════════════════════

# Background service configuration
# Format: ServiceName:service_file.py:foreground
services = SmsReceiver:service.py:foreground

# ═══════════════════════════════════════════════════════════
#           ANDROID FEATURES
# ═══════════════════════════════════════════════════════════

# Hardware features required
android.features = android.hardware.telephony

# ═══════════════════════════════════════════════════════════
#           BUILD ARCHITECTURE
# ═══════════════════════════════════════════════════════════

# CPU architectures (most phones support these)
# arm64-v8a = Modern 64-bit phones
# armeabi-v7a = Older 32-bit phones
android.archs = arm64-v8a,armeabi-v7a

# ═══════════════════════════════════════════════════════════
#           ADVANCED SETTINGS
# ═══════════════════════════════════════════════════════════

# Python activity entrypoint
android.entrypoint = org.kivy.android.PythonActivity

# Security whitelist
android.whitelist = lib-dynload/termios.so

# Accept SDK license automatically
android.accept_sdk_license = True

# Skip update check
android.skip_update = False

# Use gradle for building
android.gradle = True

# ═══════════════════════════════════════════════════════════
#           BUILDOZER CONFIGURATION
# ═══════════════════════════════════════════════════════════

[buildozer]

# Log level (0=error, 1=info, 2=debug)
log_level = 2

# Warn if running as root
warn_on_root = 1

# Build directory (temporary files)
build_dir = ./.buildozer

# Binary output directory (final APK location)
bin_dir = ./bin


# ═══════════════════════════════════════════════════════════
#           NOTES & INSTRUCTIONS
# ═══════════════════════════════════════════════════════════

# USAGE:
# ------
# 1. Is file ko "buildozer.spec" naam se save karo
# 2. Same folder mein "main.py" rakho
# 3. Terminal mein run karo:
#    $ buildozer android debug
#
# OUTPUT:
# -------
# APK file yahan banega: bin/smsforwarder-1.0-debug.apk
#
# CUSTOM ICON (Optional):
# -----------------------
# Agar apna icon lagana hai:
# 1. icon.png file banao (512x512 recommended)
# 2. Same folder mein rakho
# 3. Upar "icon.filename" line uncomment karo
#
# VERSION UPDATE:
# ---------------
# Naya version release karne ke liye:
# version = 1.1  (1.0 se 1.1 karo)
#
# ARCHITECTURES:
# --------------
# Agar sirf 64-bit phones ke liye chahiye:
# android.archs = arm64-v8a
#
# Agar purane phones bhi support karni hain:
# android.archs = arm64-v8a,armeabi-v7a  (default hai)
#
# PERMISSIONS:
# ------------
# Har permission comma se separate (NO SPACES!)
# Galat: READ_SMS, RECEIVE_SMS
# Sahi:  READ_SMS,RECEIVE_SMS
#
# ANDROID 15 SUPPORT:
# -------------------
# ✅ Target API: 35 (Android 15)
# ✅ Minimum API: 21 (Android 5.0+)
# ✅ Support range: Android 5.0 to Android 15
# ✅ Foreground service notifications
# ✅ Latest NDK (26b) for better performance
#
# COMPATIBILITY:
# --------------
# Is configuration se app chalega:
# - Android 5.0 (2014) se lekar
# - Android 15 (2024) tak
# - Total: 10+ years ke devices support!
