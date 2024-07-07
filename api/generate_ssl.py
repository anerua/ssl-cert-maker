import os
import subprocess
import argparse

def generate_certificate(domain, challenge, wildcard):
    home_dir = os.path.expanduser("~")
    output_dir = os.path.join(home_dir, "Downloads")

    if wildcard:
        challenge = "dns"
        domain = f"*.{domain}"

    command = [
        "certbot", "certonly",
        "--manual",
        "--preferred-challenges", challenge,
        "--domain", domain,
        "--config-dir", output_dir,
        "--work-dir", output_dir,
        "--logs-dir", output_dir,
        "--agree-tos",
        "--email", "aneruamartins@gmail.com"
    ]

    try:
        subprocess.run(command)
        print(f"Certificate for {domain} generated successfully and saved in {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SSL certificates using Certbot")
    parser.add_argument("domain", help="The domain name for the SSL certificate")
    parser.add_argument("--challenge", choices=["http", "dns"], default="http", help="The preferred challenge method")
    parser.add_argument("--wildcard", action="store_true", help="Generate a wildcard certificate")

    args = parser.parse_args()

    if args.wildcard and args.challenge != "dns":
        print("Wildcard certificates require DNS challenge method. Overriding challenge method to 'dns'.")
        args.challenge = "dns"

    generate_certificate(args.domain, args.challenge, args.wildcard)

# Usage:
    # Example: using HTTP challenge
    # python generate_ssl.py example.com --challenge http

    # Example: for a wildcard certificate
    # python generate_ssl.py example.com --wildcard