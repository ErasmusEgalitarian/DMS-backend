import ssl
print("SSL module available:", hasattr(ssl, "create_default_context"))
print("SSL version:", ssl.OPENSSL_VERSION)
print("Default CA certs path:", ssl.get_default_verify_paths())
