[app]

# Basic Information
title = SMS Forwarder
package.name = smsforwarder
package.domain = org.example

# Source
source.dir = .
source.include_exts = py
version = 1.0

# Requirements
requirements = python3,kivy==2.2.1,pyjnius,requests,android

# Permissions
permissions = INTERNET,READ_SMS,RECEIVE_SMS,SEND_SMS,READ_CONTACTS,READ_PHONE_STATE,POST_NOTIFICATIONS,FOREGROUND_SERVICE
android.permissions = INTERNET,READ_SMS,RECEIVE_SMS,SEND_SMS,READ_CONTACTS,READ_PHONE_STATE,POST_NOTIFICATIONS,FOREGROUND_SERVICE

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
p4a.branch = master

# Architecture  
android.archs = arm64-v8a,armeabi-v7a

# Orientation
orientation = portrait
fullscreen = 0

[buildozer]

# Log level
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aar, .aab) storage
bin_dir = ./bin
