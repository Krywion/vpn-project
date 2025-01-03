import os

def main(option):
    if option == "-h" or option == "--help":
        print("Usage: vpn-connect.py [OPTION]")
        print("Connect to the VPN server")
        print("Options:")
        print("  -h, --help    display this help and exit")
        return
    if option == "-l" or option == "--list":
        print("Available VPN servers:")
        
        return

if __name__ == "__main__":
    main(sys.argv[1])