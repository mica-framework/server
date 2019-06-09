#!/bin/bash

# we just need a certificate for the registry
mkdir -p certs; cd certs;

# now create the certificate
openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 365 -out domain.crt

