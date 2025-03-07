# minecraft_server
This Python script is a Minecraft server manager that allows you to easily download, configure and manage a Minecraft server.

It's just a prototype, not to call it crap, there are a lot of things missing, but I think this project was fun for me. I know that the script is in spanish, very soon, not to say in months, I will update everything when I can.
Before this, it is worth mentioning that you need python3 and java installed.

Main features:

    Automatic server download.
        Gets the version list from the Mojang API.
        Downloads the server.jar of the selected version.

    Organized folder structure
        Creates directories like mods, world, datapacks, config, logs and backups to keep the server tidy.

    Customizable settings
        Allows you to choose the server difficulty (peaceful, easy, normal, hard).

    Server management
        Start the server with subprocess.
        Accept automatically the Mojang EULA.
        Displays public IP for easy access to the server.

    Interactive menus
        Initial menu to manage versions.
        Advanced configuration menu

IF YOUR IP DOES NOT WORK, READ THIS:

  Public IP and Port Forwarding
        The public IP of your PC must be accessible from the Internet. You can verify it with your script (get_public_ip()).
        You need to open (forward) port 25565 on your router. Look for the Port Forwarding option in the router configuration and forward it to the local IP of your PC.

    Firewall Settings
        Make sure to allow traffic on port 25565 in your operating system's firewall.

    Server Settings
        In the server.properties file, change server-ip= and leave it empty to accept any IP.

    Player Connection
        Your friends must connect using your public IP (for example, 123.45.67.89:25565).
        If they play on the same local network, they can use your private IP (LAN).

⚠ Note: If your public IP is dynamic, it may change over time. You can use a dynamic DNS service (such as No-IP or DuckDNS) so that your friends always connect to a domain instead of a changing IP.
