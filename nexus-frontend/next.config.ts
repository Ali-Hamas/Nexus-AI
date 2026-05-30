import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow the dev server to serve HMR + framework assets to both 127.0.0.1
  // and the LAN IP (so phones / other devices on the network can hit it too).
  // Without this, Next 16 blocks dev resources from any host that isn't `localhost`,
  // which prevents React from hydrating and makes onClick handlers do nothing.
  allowedDevOrigins: [
    "127.0.0.1",
    "localhost",
    "192.168.157.213",
  ],
};

export default nextConfig;
