# cdr-receiver
A simple CDR receiver implementation for Cisco Meeting Server

#### usage
```bash
python app.py -p <port> [-c <certfile path>] [-k <keyfile path>]
```

The receiver supports both HTTP and HTTPS. To use HTTP launch the app with the ``` -p ``` flag and specify the desired port.

```bash
python app.py -p 8444
```

To use the receiver with HTTPS you'll need a key and certtificate pair.

#### self signed certificate generation

```bash
openssl req -newkey rsa:2048 -nodes -keyout receiver.key -x509 -days 365 -out receiver.crt
```
```
Generating a 2048 bit RSA private key
............................................+++
.............................................................................................+++
writing new private key to 'receiver.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:US
State or Province Name (full name) []:New York
Locality Name (eg, city) []:New York
Organization Name (eg, company) []:Cisco
Organizational Unit Name (eg, section) []:lab
Common Name (eg, fully qualified host name) []:receiver.lab.cisco.com
Email Address []:cert@lab.cisco.com
```

Fill out the CSR questionnaire and you are all set.

Now that you have a key and certificate you can use the receiver over HTTPS.

```bash
python app.py -p 8443 -c receiver.crt -k receiver.key
```

#### meeting server configuration
From webadmin on Cisco Meeting Server navigate to: Configuration > CDR Settings

In one of the four Receiver URI slots enter the URI for host that is running the receiver.

``` https://receiver.lab.cisco.com:8443 ```

#### testing
Start a meeting on CMS. The raw XML from the CDR event will be printed to the console.


```
using protocol version: HTTP/1.1
HTTPS mode with certfile cdr.crt
received request for POST /
data: <?xml version="1.0"?>
  <records session="290da844-0ebd-4b42-8049-e264375f1d33">
    <record type="callStart" time="2019-04-04T15:28:37Z" recordIndex="1" correlatorIndex="6">
    <call id="634f5879-6907-429d-949a-ef630079cdbe">
      <name>Kashyyyk Civil Engineering</name>
      <ownerName></ownerName>
      <callType>coSpace</callType>
      <coSpace>6bbd1f1f-2bc0-44d8-9cba-73ebd5bc2657</coSpace>
      <callCorrelator>9f302948-f856-4c7f-8655-d45e4de22a8e</callCorrelator>
    </call>
  </record>
</records>
```
