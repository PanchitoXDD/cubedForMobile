[app]
title = CUBED
package.name = cubed
package.domain = io.cubedgame
source.dir = .
source.include_exts = py,ogg,mp3,json,txt
source.exclude_dirs = .git,.github,.buildozer,bin
version = 0.2.21
requirements = python3,pygame-ce
orientation = landscape
fullscreen = 1
android.api = 36
android.minapi = 23
android.ndk = 29
android.archs = arm64-v8a
android.accept_sdk_license = True
android.private_storage = True
android.debug_artifact = apk
p4a.branch = develop
p4a.bootstrap = sdl2
p4a.local_recipes = ./p4a-recipes

[buildozer]
log_level = 2
warn_on_root = 0
