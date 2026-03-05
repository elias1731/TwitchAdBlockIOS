#import <AVFoundation/AVFoundation.h>

%hook AVURLAsset

- (instancetype)initWithURL:(NSURL *)URL options:(NSDictionary<NSString *, id> *)options {
    // Pr�fen, ob es sich um den Twitch Live-Stream HLS Endpunkt handelt
    if ([URL.host isEqualToString:@"usher.ttvnw.net"] && [URL.path hasPrefix:@"/api/channel/hls/"]) {
        
        // Kanalnamen aus dem URL-Pfad extrahieren (z.B. "kanalname.m3u8" -> "kanalname")
        NSString *channel = [[URL.lastPathComponent stringByDeletingPathExtension] lowercaseString];
        
        // Neue Luminous-Proxy URL bauen
        NSString *newURLString = [NSString stringWithFormat:@"https://eu.luminous.dev/", channel];
        NSURL *newURL = [NSURL URLWithString:newURLString];
        
        // Das modifizierte Asset laden
        return %orig(newURL, options);
    }
    
    return %orig;
}

%end
