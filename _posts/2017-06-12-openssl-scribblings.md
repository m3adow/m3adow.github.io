---
layout: default
title: "OpenSSL scribblings"
categories:
- ssl
- linux
---

Just a quick writeup from my notes so I know where to look it up if I ever search for it again. In my examples I use Comodo as the certificate authority and ssl.example.org as domain.

# Certificate chain verification

There are two scenarios I normally encounter, either verify if the certificate chain is complete or find out where the certificate chain breaks.

##Verifying the whole chain
1. Concatenate the certificate chain including the root certificate in one file. From the top of my head I'm not quite certain if order is important, leaf to root worked for me.
2. Do an `openssl verify` with `-CApath /dev/null` to prevent taking the systems trust stores into account:

```bash
openssl verify -verbose -CApath /dev/null -CAfile concatenated-chain-file.pem ssl.example.org.crt
```
If the output of the command contains 'OK', the chain is complete.

##Verifying the certificate chain partially

If the certificate chain is not complete, there are two ways to find out which part didn't fit. The easier one needs OpenSSL 1.0.2g or later which is not easily available for many systems still in use, like RHEL 6 or Ubuntu 14.04. As I haven't encountered this requirement too often, it's not very elaborate.

###Via "openssl verify -partial_chain" (OpenSSL version >= 1.0.2g)

Do this for every part of the chain you want to test:

```bash
openssl verify -CApath /dev/null -partial_chain -trusted addtrustexternalcaroot.crt comodorsaaddtrustca.crt
```

###Manual

If OpenSSL 1.0.2g is not available or more output is required, you can do this, assuming you have all the certificate chain certs in one dir ending with `.crt`:

```bash
for FILE in $(ls *.crt); do openssl x509 -noout -text -in ${FILE} | grep "Key Identifier" -A1
```

This will output the AKI and SKI of the cert. SKI of the Root CA needs to be identical to the AKI of the following Intermediate CA, etc.

#Verify match of private key and certificate or CSR

To verify the match of a private key, certificate or CSR, compare the modulus of the file.

```bash
openssl x509 -noout -modulus -in test.crt
openssl req -noout -modulus -in test.csr
openssl rsa -noout -modulus -in test.key
```

Comparing the md5sum of the openssl output eases the process.

```bash
openssl x509 -noout -modulus -in test.crt | openssl md5
openssl req -noout -modulus -in test.csr | openssl md5
openssl rsa -noout -modulus -in test.key | openssl md5
```

To compare 2 files easily, this one-liner can be used.

```bash
MYDOM=ssl.example.org
[[ "$(openssl x509 -noout -modulus -in ${MYDOM}.crt |openssl md5)" == "$(openssl rsa -noout -modulus -in ${MYDOM}.key | openssl md5)" ]] && echo "OK" || echo "NOT OK"
```

#Using s_client

The only real interesting thing about `openssl s_client` I can think of from the top of my head is the fact that feeding `/dev/null` as input eases piping.

```bash
openssl s_client -connect ssl.example.org:443 < /dev/null | openssl x509 -noout -text
```

If I remember or encounter more tasks I don't do on a daily basis and therefore forget regularly, I will extend this list.