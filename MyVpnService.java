public class MyVpnService extends VpnService {
    @Override
    public void onStartCommand(Intent intent, int flags, int startId) {
        Builder builder = new Builder();
        builder.addAddress("10.0.0.2", 24); // Example IP for device
        builder.addDnsServer("1.1.1.1");    // Cloudflare DNS
        builder.addDnsServer("1.0.0.1");
        builder.addRoute("0.0.0.0", 0);     // Route all traffic
        ParcelFileDescriptor vpnInterface = builder.establish();

        // Then connect socket to your server's IP:5001
        // Exchange messages per your Python server protocol
        // Forward data between vpnInterface and the socket
    }
}