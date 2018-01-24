README

This file describes the topology and addressing scheme for our IoT
device testbed.  

Current Devices

Our testbed is currently comprised of the following devices:

| Device             | MAC Address              |                        IP Address |
|--------------------+--------------------------+-----------------------------------|
| Monitoring server  | 00:1d:92:b6:f1:2d        |            192.168.1.10, 10.0.6.2 |
| TP-Link Router     | f8:d1:11:2f:59:38  (LAN) | 192.168.1.1, 10.0.{1,2,3,4,5,6}.1 |
| Amazon Echo        | 40:b4:cd:41:cb:d5        |                          10.0.2.2 |
| Google Chromecast  | f4:f5:d8:0a:3e:04        |                          10.0.3.2 |
| Dahua IP Camera    | 3c:ef:8c:a3:75:51        |                          10.0.4.2 |
| TP-Link Smart Plug | 50:c7:bf:33:33:78        |                          10.0.5.2 |

**NOTE**: The above mapping does NOT apply to the initial setup traces
  included in the initial_traces directory.  For the correct IP
  addresses for devices during initial setup, see README-INITIAL.txt
  in the intiail_traces directory.

Capture file notes

 - In order to measure traffic sent between devices, we place each
   device in its own /30 subnet such that all traffic must be sent to
   the router (where it is captured) before being sent to other
   devices.  A side-effect of this architecture is that all
   inter-device traffic is currently duplicated in our packet captures,
   since the interface being mirrored records the packet entering and
   leaving the router's LAN interface.  Thus, any measurements
   performed on traffic sent *between* IoT devices will need to first
   filter out these duplicate packets.  


Observations on device traffic

Chromecast
 - All communication with Google happens over TLS.  The idle behavior
   for the Chromecast is to display a "screen saver" of top photos
   from sites like Google+ and 500px.  These photos appear to be
   downloaded periodically from Google (over TLS), generating about
   10-20MB of traffic per hour.  Notably, our Chromecast isn't bound
   to a Google account--if we had done this, I think it would fetch
   the photos from the user's Google Photos profile instead of from a
   list of top photos.
 - Our Chromecast seems to ignore our DHCP server's settings for a DNS
   server in favor of Google Public DNS (8.8.8.8).  This has
   interesting implications for privacy since it means that the device
   will not use an ISP's default DNS server, making it harder for an
   ISP to hijack or gather information on queries made by the device
   (since the ISP would need to capture DNS traffic instead of just
   leveraging a DNS server).  On the other hand, it means that Google
   can use their DNS infrastructure to do their own analytics on
   queries, or use the protocol in off-spec ways as a control or
   side-channel.  For example, the Chromecast makes queries for the
   domain "channel.status.request.url"--a bogus TLD.  The
   server responds appropriately with NXDOMAIN, but it seems likely
   that this kind of query is intended as a heartbeat signal.

Echo
 - Like the Chromecast, all communication with Amazon's servers seems
   to happen over TLS.  The exception is a periodic HTTP connection to
   an Amazon server to verify Internet connectivity.  

Smart plug
 - All of the periodic traffic I've observed so far appears to be
   NTP.
 - At the moment, control of the smart plug appears to happen
   locally--without involvement of a cloud service.  I believe there
   are settings to configure this, which I will be investigating for
   the next set of tests.

Camera
 - In the present (default) configuration, the camera doesn't appear
   to generate any external traffic.
