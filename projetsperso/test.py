import ssl
print((ssl.OPENSSL_VERSION_INFO < (1,1,1)) or  (not ssl.OPENSSL_VERSION.startswith("OpenSSL ")))