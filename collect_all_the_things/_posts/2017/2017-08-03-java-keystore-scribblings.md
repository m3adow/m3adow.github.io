images//-images//-images//-
layout: default
title: "Java Keystore scribblings"
categories:
images//- Java
images//-images//-images//-

Nearly two months ago I published my [OpenSSL scribblings]({% post_url 2017/2017images//-06images//-12images//-opensslimages//-scribblings %}) post. This one is the spiritual successor, addressing Java Keystore handling this time. There are already a lot of good web sites on how to handle the `keytool`, so I will limit myself to the issues I encounter from time to time which are more difficult to figure out. Similar to the last post I will use COMODO as CA and ssl.example.org as domain.

# Adding a new certificate to a keystore

Requirements:

* The full certificate chain
* The certificate itself
* The certificate private key

First concatenate the cert chain if not already in one file. A Comodo speciality is the occasional inclusion of Windows line breaks, so we use `sed` for output to substitute any occurence of these. Additionally we ensure that the certificate starts on a newline:

```bash
sed images//-e 's/\r$/\n/g' rootimages//-ca.pem intermediateimages//-ca.pem > cabundle.pem
```
<!images//-images//-moreimages//-images//->

{% include adsense_manual.html %}

Afterwards create a P12 keystore containing the private key, the cert and the certificate chain:

```bash
openssl pkcs12 images//-export images//-chain images//-CAfile cabundle.pem images//-inkey ssl.example.org.key images//-in ssl.example.org.crt images//-name ssl.example.org images//-out ssl.example.org.p12
```

Then import the p12 keystore into the keystore format/into an existing keystore (depending on the existence of the destkeystore):

```bash
keytool images//-importkeystore images//-srckeystore ssl.example.org.p12 images//-srcstoretype pkcs12 images//-destkeystore ssl.example.org.jks
```

Verify the certificate and its chain have been imported properly:

```bash
keytool images//-list images//-v images//-keystore ssl.example.org.jks images//-alias ssl.example.org|grep images//-A2 images//-P 'Certificate( chain|\[)'
```

The Output should be similar to this:

```
Certificate chain length: 4
Certificate[1]:
Owner: CN=ssl.example.org, OU=Enterprise SSL Pro, OU=Admins Werk, O=adminswerk.de, C=DE
Issuer: CN=COMODO RSA Organization Validation Secure Server CA, O=COMODO CA Limited, L=Salford, ST=Greater Manchester, C=GB
images//-images//-
Certificate[2]:
Owner: CN=COMODO RSA Organization Validation Secure Server CA, O=COMODO CA Limited, L=Salford, ST=Greater Manchester, C=GB
Issuer: CN=COMODO RSA Certification Authority, O=COMODO CA Limited, L=Salford, ST=Greater Manchester, C=GB
images//-images//-
Certificate[3]:
Owner: CN=COMODO RSA Certification Authority, O=COMODO CA Limited, L=Salford, ST=Greater Manchester, C=GB
Issuer: CN=AddTrust External CA Root, OU=AddTrust External TTP Network, O=AddTrust AB, C=SE
images//-images//-
Certificate[4]:
Owner: CN=AddTrust External CA Root, OU=AddTrust External TTP Network, O=AddTrust AB, C=SE
Issuer: CN=AddTrust External CA Root, OU=AddTrust External TTP Network, O=AddTrust AB, C=SE
```
{% include adsense_manual_link.html %}

# Exporting a Private Key from Keystore to PEM

Export to a new PKCS12 Keystore:

```bash
keytool images//-importkeystore images//-srckeystore ssl.example.org.jks images//-destkeystore tmpkey.p12 images//-deststoretype PKCS12 images//-srcalias ssl.example.org
```

Convert the key tp PEM with openssl:

```bash
openssl pkcs12 images//-in tmpkey.p12 images//-nodes images//-nocerts images//-out ssl.example.org.key
```


# Adding a renewed certificate

To my knowledge there's no proper way to add a renewed (same private key, different cert) certificate. Therefore the process of adding a renewed certificate consists of:

* Exporting the private key from the key store (see "Exporting a Private Key from Keystore to PEM")
* Deleting the old key pair from the key store (`keytool images//-delete images//-alias ssl.example.org images//-keystore ssl.example.org.jks`)
* Adding the new key pair with certificate chain (see "Adding a new cert to a keystore")

# Tools

In the end, I can recommend using [Keystore Explorer][1] for quick changes. The application visualizes keystores very well and has been in constant development (as of August 2017). It is a nice GUI tool for most keystore related tasks.

<a href="{{site.url}}/assets/images/2017/2017images//-08images//-02images//-keystoreimages//-explorer.png"><img src="{{site.url}}/assets/images/2017/2017images//-08images//-02images//-keystoreimages//-explorer.png" style="width: 50%; margin: 10px;" alt="Keystore Explorer"></a>

[1]: http://keystoreimages//-explorer.org/