Notes on initial setup captures

The initial packet captures for the Echo and Chromecast were made
prior to adding /30 subnets for each host.  In these captures, the
Echo and Chromecast have addresses in a single subnet, as noted in the
table below.  During this period, we were not testing any
functionality that required inter-device communication.

| Device             | MAC Address              |                      IP Address |
|--------------------+--------------------------+---------------------------------|
| Monitoring server  | 00:1d:92:b6:f1:2d        |          10.0.1.2, 192.168.1.10 |
| TP-Link Router     | f8:d1:11:2f:59:38  (LAN) | 192.168.1.1, 10.0.{1,2,3,4,5}.1 |
| Amazon Echo        | 40:b4:cd:41:cb:d5        |                   192.168.1.219 |
| Google Chromecast  | f4:f5:d8:0a:3e:04        |                   192.168.1.120 |
| Dahua IP Camera    | 3c:ef:8c:a3:75:51        |                        10.0.4.2 |
| TP-Link Smart Plug | 50:c7:bf:33:33:78        |                        10.0.5.2 |

Capture files from the initial setup are not precisely annotated with user
events.  However, a summary of the actions performed on each device is
as follows.  You can get an approximate timestamp for some of the
actions by examining the DNS queries made by each device.

 - Chromecast
   - Played a handful of distinct Youtube videos
   - Played a twitch.tv stream
   - Streamed a tab from Chrome (content was a Wikipedia page)
 - Echo
   - Made several search-based voice queries ("What is the distance to
     the moon?"  "Roll a N-sided die", etc.)
   - Played multiple some radio streams (NPR, WBRU)
 - Smart plug
   - Toggled plug on and off (via app and button)
 - Camera
   - Accessed web interface and installed viewing plugin
   - Streamed video to a windows client

Other interesting notes
 - At initialization, the Echo downloads a firmware update over HTTP.
   You can extract the payload of the HTTP request, which yields a
   signed APK.  I haven't tried to reconstruct the device's
   filesystem from this yet, but it should be possible. 
- More observations on the general behavior of the devices is included
  in README-TOPOLOGY.txt.
