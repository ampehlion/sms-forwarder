[app]
title = SMS Forwarder
package.name = smsforwarder
package.domain = org.example
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy,pyjnius,requests,android
permissions = INTERNET,READ_SMS,RECEIVE_SMS,SEND_SMS,READ_CONTACTS,READ_PHONE_STATE
android.permissions = INTERNET,READ_SMS,RECEIVE_SMS,SEND_SMS,READ_CONTACTS,READ_PHONE_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
