[app]
title = Note Sorter
package.name = notesorter
package.domain = org.example.notesorter
source.dir = .
source.include_exts = py,kv,txt,db
version = 0.1
requirements = python3,kivy,plyer
orientation = portrait
fullscreen = 0

# Ensure permissions for file access
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Optional: Use latest API and supported archs
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

# Disable backup prompt on Android
android.allow_backup = 1

# Optional: UI tweaks
android.presplash_color = #1a1a33
android.hide_statusbar = 0

# Include database file if needed
# Note: recommended to let SQLite generate a fresh one in user_data_dir

# If you want to keep logcat clean
log_level = 2

# If using ADB debugging or USB
android.adb_port = 5037

[buildozer]
log_level = 2
warn_on_root = 1
