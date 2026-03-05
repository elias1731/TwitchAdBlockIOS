ifeq ($(SIDELOADED),1)
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
