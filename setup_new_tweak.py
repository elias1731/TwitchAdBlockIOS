import os
import shutil

# Dateien und Ordner, die zwingend erhalten bleiben müssen
KEEP = {
    '.git', 
    '.github', 
    '.gitignore', 
    'control', 
    'TwitchAdBlock.plist', 
    'setup_new_tweak.py'
}

print("Räume altes Projekt auf...")
# Lösche alles, was nicht in KEEP definiert ist
for item in os.listdir('.'):
    if item in KEEP:
        continue
    
    if os.path.isdir(item):
        shutil.rmtree(item)
        print(f"Ordner gelöscht: {item}")
    else:
        os.remove(item)
        print(f"Datei gelöscht: {item}")

print("Erstelle neues Makefile...")
makefile_content = """ifeq ($(SIDELOADED),1)
MODULES = jailed
endif

PACKAGE_VERSION = 2.0.0
ifdef APP_VERSION
  PACKAGE_VERSION := $(APP_VERSION)-$(PACKAGE_VERSION)
endif

TARGET := iphone:clang:latest:14.0
INSTALL_TARGET_PROCESSES = Twitch
ARCHS = arm64

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = TwitchAdBlock
$(TWEAK_NAME)_FILES = Tweak.x
$(TWEAK_NAME)_CFLAGS = -fobjc-arc

ifeq ($(SIDELOADED),1)
  CODESIGN_IPA = 0
endif

include $(THEOS_MAKE_PATH)/tweak.mk
"""
with open('Makefile', 'w') as f:
    f.write(makefile_content)

print("Erstelle neue Tweak.x...")
tweak_content = """#import <AVFoundation/AVFoundation.h>

%hook AVURLAsset

- (instancetype)initWithURL:(NSURL *)URL options:(NSDictionary<NSString *, id> *)options {
    // Prüfen, ob es sich um den Twitch Live-Stream HLS Endpunkt handelt
    if ([URL.host isEqualToString:@"usher.ttvnw.net"] && [URL.path hasPrefix:@"/api/channel/hls/"]) {
        
        // Kanalnamen aus dem URL-Pfad extrahieren (z.B. "kanalname.m3u8" -> "kanalname")
        NSString *channel = [[URL.lastPathComponent stringByDeletingPathExtension] lowercaseString];
        
        // Neue Luminous-Proxy URL bauen
        NSString *newURLString = [NSString stringWithFormat:@"https://eu.luminous.dev/live/%@?allow_source=true&allow_audio_only=true&fast_bread=true", channel];
        NSURL *newURL = [NSURL URLWithString:newURLString];
        
        // Das modifizierte Asset laden
        return %orig(newURL, options);
    }
    
    return %orig;
}

%end
"""
with open('Tweak.x', 'w') as f:
    f.write(tweak_content)

print("Fertig! Das Repository ist jetzt clean und der neue Tweak ist einsatzbereit.")
