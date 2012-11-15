#!/bin/python

import cherrypy
import os, socket
import shlex, subprocess
import tempfile
import random

class CertBot(object):
    
    def __init__(self, working_dir=None, ca_key=None, ca_key_pass=None, ca_config=None):
        self.working_dir = working_dir
        self.ca_key = ca_key
        self.ca_key_pass = ca_key_pass
        self.ca_config = ca_config


    @cherrypy.expose
    def index(self):
        return """
               <h1><a href='/'>{hostname} CertBot</a></h1>
               <p>CertBot is a training CA, designed to show you how to generate and sign x509 certificates.</p>
               <p>This is a three step process for getting a signed Certificate. Gennerly Step 3 in the process
                  is handled entirely by your Certficate Authority, and completely abstracted from you. 
                  <ul>
                      <li>The first two steps (links) will direct you through the process of crating an x509 certificate request.</li>
                      <li>The thirds step (link) shows you how to provide this request to the CA of your choosing and what is 
                          typicaly done with the request before it is returned to you as a Certificate.</li>
                  </ul>
                  All of the commands used in these examples use OpenSSL because it allows you to use the base SSL objects.
               </p>
               <ol>
                   <li><a href="/Request_Key">Request a Key</a></li>
                   <li><a href="/Request_Cert">Request a Certificate</a></li>
                   <li><a href="/Sign_Cert">Sign a Certificate Request</a></li>
                   <li><a href="/Config_CA">Setup your OpenSSL CA</a></li>
               <ol>
               """.format(hostname=socket.gethostname())


    @cherrypy.expose
    def Request_Key(self):
        return """
               <h2><a href='/'>{hostname}</a> Key Request</h2>
               <form action="Requested_Key" method="POST">
               Key Password: <input type="text" name="password" value="password">
               <input type="submit">
               </form>
               <p>Generly the first step in Creating a certificate request is creating a public/private key pair. <br>
                  These key are used in the encryption and decryption of data. With x509 certifates or PKI keys 
                  these keys can also be used to determin the identity of an entity (known as a signature).</p>
               """.format(hostname=socket.gethostname())

        
    @cherrypy.expose
    def Request_Cert(self):
        return """
               <h2><a href='/'>{hostname}</a> Certificate Request</h2>
               <p>Certificate Requests are simply your way of pairing your Identity with your encryption keys.<br>
                  x509 Certificates are often compared to state issued ID's, making Certificate Requests your application
                  for an ID.</p>
               <p>Complete the form to genereate a certificate request. Please note '*'ed fields are required</p>
               <form action="Requested_Cert" method="POST">
                Country     :<input type="text" name="country" value="US">*<br>
                State       :<input type="text" name="state" value="North_Carrolina">*<br>
                City        :<input type="text" name="city" value="Raleigh">*<br>
                Orginization:<input type="text" name="org" value="Red_Hat_Inc">*<br>
                Department  :<input type="text" name="orgUnit" value="Global_Support_Services">*<br>
                Common Name :<input type="text" name="commonName" value="">*<br>
                Email       :<input type="text" name="email" value="">*<br>
                Key: * <br>
                <textarea name="key" rows="30" cols="82"></textarea><br>
                Password    :<input type="text" name="password" value=""> This is the password for the key.<br>
                <input type="submit">
               </form>
               """.format(hostname=socket.gethostname())


    @cherrypy.expose 
    def Sign_Cert(self):
        return """
                <h2><a href='/'>{hostname}</a> Certificate Signing Authority</h2>
                <p>Once you have a Certificate Request you simply need to have someone vouch for your identity.<br>
                   The most common ways of doing this are trough Certificate Authorities or Web's of Trust.<br>
                   Web's of trust involve a more active form of participation which is why Certifiate Authorities are prefered.</p>
                <form action="Signed_Cert" method="POST">
                <textarea name="certificate" rows="35" cols="82">Certificate</textarea><br>
                <input type="submit">
                </form>""".format(hostname=socket.gethostname())


    def isValid_Req(self, certificate):       # Internal to Application (Do NOT Expose)
       cert_expected_header = "-----BEGIN CERTIFICATE REQUEST-----"
       cert_expected_tail   = "-----END CERTIFICATE REQUEST-----"
       key_expected_header  = "-----BEGIN RSA PRIVATE KEY-----"
       key_expected_tail    = "-----END RSA PRIVATE KEY-----"

       header = certificate[:35]                     # A CSR should start with this.
       tail = certificate[-33:len(certificate)]      # A CSR should end with this. 
       if header == cert_expected_header and tail == cert_expected_tail:
           return True
       else:
           pass
           # TODO: LOGGING
           #print 'Header ({0}): "{1}"'.format(len(header), header)
           #print 'Expect ({0}): "{1}"'.format(len(cert_expected_header), cert_expected_header)
           #print 'Tail ({0}): "{1}"'.format(len(tail), tail)
           #print 'Expc ({0}): "{1}"'.format(len(cert_expected_tail), cert_expected_tail)

       header = certificate[:31]                     # A CSR should start with this.
       tail = certificate[-29:len(certificate)]      # A CSR should end with this. 
       if header == key_expected_header and tail == key_expected_tail:
           return True
       else:
           pass
           # TODO: LOGGING
           #print 'Header ({0}): "{1}"'.format(len(header), header)
           #print 'Expect ({0}): "{1}"'.format(len(key_expected_header), key_expected_header)
           #print 'Tail ({0}): "{1}"'.format(len(tail), tail)
           #print 'Expc ({0}): "{1}"'.format(len(key_expected_tail), key_expected_tail)
       return False


    @cherrypy.expose
    def Requested_Key(self, password=None):
        if password == None or password == "":
            raise cherrypy.HTTPError("501 Not Implemented", "Password must be suplied for your key, while it is not generly a requirement it is recomended.")
        else:
            key_command = "openssl genrsa -des3 -passout pass:{key_pass} 2048".format(key_pass=password)
        
            (out, err) = subprocess.Popen(shlex.split(key_command), stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()   # Run the Command.
            out = "<br>".join(out.split(os.linesep)) # This turns the output into HTML...(readable format)
            return """
                   <h2><a href='/'>{hostname}</a> Private Key</h2>{key}<br>
                   <b>This key should be coppied and placed into a file. The convention is to name that file with a '.key' exstention.</b><br>
                   You will want every thing from '-----BEGIN RSA PRIVATE KEY-----' to '-----END RSA PRIVATE KEY-----'. 
                   Remember this is priave and should not be shared.<br>
                   Created with: <b>{command}</b>
                   """.format(hostname=socket.gethostname(), key=out, command=key_command)
                                                       
                                                       
    @cherrypy.expose                                   
    def Requested_Cert(self, country=None, state=None, city=None, org=None, orgUnit=None, commonName=None, email=None, key=None, password=None):
        req_command_org = "openssl req -new -key {key_file} -passin pass:{key_pass} -config {req_config} -batch"
        config_handle = tempfile.NamedTemporaryFile(dir=self.working_dir, delete=False)
        config = """
        [ req ]
        default_bits           = 1024
        distinguished_name     = req_distinguished_name
        prompt                 = no

        [ req_distinguished_name ]
        C                      = {CO}
        ST                     = {ST}
        L                      = {LO}
        O                      = {OG}
        OU                     = {OU}
        CN                     = {CN}
        emailAddress           = {EM}
        """.format(CO=country, ST=state, LO=city, OG=org, OU=orgUnit, CN=commonName, EM=email)
        config_handle.write(config)
        config_handle.close()

        key_handle = tempfile.NamedTemporaryFile(delete=False)
        key_handle.write(key)
        key_handle.close()

        if country == None or state == None or city == None or org == None or orgUnit == None or commonName == None or key == None or password == None:
            raise cherrypy.HTTPError("501 Not Implemented", "Requested fields can not be blank.")
        elif country == "" or state == "" or city == "" or org == "" or orgUnit == "" or commonName == "" or key == "" or password == "":
            raise cherrypy.HTTPError("501 Not Implemented", "Requested fields can not be blank.")
        elif  self.isValid_Req(key):
            req_command = req_command_org.format(key_file=key_handle.name, req_config=config_handle.name, key_pass=password)
            (out, err) = subprocess.Popen(shlex.split(req_command), stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()   # Run the Command.
            out = "<br>".join(out.split(os.linesep)) # This turns the output into HTML...(readable format)
            os.unlink(config_handle.name)                                                  # Delete the config.
            os.unlink(key_handle.name)                                                     # Delete the Keyfile.
        else:
            raise cherrypy.HTTPError("501 Not Implemented", "Key must be a vaild Key.")

        req_command = req_command_org.format(key_file="my_private.key", req_config="provided.conf", key_pass=password)
        html_config = "<br>".join(config.split(os.linesep)) # This turns the output into HTML...(readable format)

        return """
               <h2><a href='/'>{hostname}</a> Certificate Request</h2><br>
               {certificate}<br>
               <b>This Certificate Request (CSR) should be coppied and placed into a file. The convention is to name that file with a '.csr' exstention.</b>
               <br>Configuration:<br>{config}<br>
               Created with: <b>{command}</b>
               """.format(hostname=socket.gethostname(), certificate=out, config=html_config, command=req_command)


    @cherrypy.expose
    def Signed_Cert(self, certificate=None):
        if certificate == None or certificate == "":
            raise cherrypy.HTTPError("501 Not Implemented", "Server Certificate can not be blank.")
        elif  self.isValid_Req(certificate):
            # Neet to create a file for your request... openssl only accepts files. TEMPFILE
            csr_handle = tempfile.NamedTemporaryFile(delete=False)
            csr_handle.write(certificate)
            csr_handle.close()
            # Build a command to be run with openssl
            sign_command = "openssl ca -in {CSR} -config {config} -passin pass:{key_pass} -batch".format(
                            key_pass=self.ca_key_pass, config=self.ca_config, CSR=csr_handle.name)
            (out, err) = subprocess.Popen(shlex.split(sign_command),
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()   # Run the Command.
            os.unlink(csr_handle.name)                                                  # Delete the CSR.
            out = "<br>".join(out.split(os.linesep)) # This turns the output into HTML...(readable format)
            
            # This is here to mask the CA Private key password from the web interface 
            sign_command = "openssl ca -in {CSR} -config {config} -passin pass:{key_pass} -batch".format(
                            key_pass=self.ca_key_pass, config=self.ca_config, CSR=csr_handle.name)
            return_string = """<h2>Certificate</h2>{ssl_out}<br>Command used to generate: <b>{command}</b><br>
                            """.format(command=sign_command, ssl_out=out)  
        else:
            raise cherrypy.HTTPError("501 Not Implemented", "Server Certificate is not valid please check the certificate and resubmit.")
        
        return return_string


    @cherrypy.expose
    def Config_CA(self):
        config_path = self.ca_config
        config_handle = open(config_path, 'r')
        configuration = config_handle.read()
        config_handle.close()
     
        configuration = "<br>".join(configuration.split(os.linesep))
        return """
               <h2><a href='/'>{hostname}</a> Certificate Request</h2>
               <p>If you wish to set up your own openssl CA you can use the following CA configuration:</p>
               {config}
               """.format(hostname=socket.gethostname(), config=configuration) 


# ====THE SET UP=====You need all of this infrastructure===================================================================
CA_key_password = "certbot"

# Set up a Temp CA dirs and files
ca_dir = tempfile.mkdtemp()              
print "Temporary Working Directory: {dir} [Delete after restart or shutdown]".format(dir=ca_dir)

os.mkdir(ca_dir + os.sep + "certs")              # May not need this 
os.mkdir(ca_dir + os.sep + "crl")                # May not need this 
os.mkdir(ca_dir + os.sep + "newcerts")           # May not need this 
os.mkdir(ca_dir + os.sep + "private")            # May not need this if you change key dir.

db_handle = tempfile.NamedTemporaryFile(dir=ca_dir, suffix=".txt", delete=False)
db_handle.close()
#print "Index: {file_name}".format(file_name=db_handle.name)

serial_handle = tempfile.NamedTemporaryFile(dir=ca_dir, delete=False)
serial_handle.write("01")
serial_handle.close()
#print "Serial: {file_name}".format(file_name=serial_handle.name)

rand_handle = tempfile.NamedTemporaryFile(dir=ca_dir, delete=False)
rand_handle.write(str(random.randint(1, 100)))
rand_handle.close()
#print "Random: {file_name}".format(file_name=rand_handle.name)

ca_key_file_name = ca_dir + os.sep + "private" + os.sep + "ca.key"
ca_key_command = "openssl genrsa -des3 -passout pass:{key_pass} -out {ca_key_file} 2048".format(key_pass=CA_key_password, ca_key_file=ca_key_file_name)

(out, err) = subprocess.Popen(shlex.split(ca_key_command), stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

config_handle = tempfile.NamedTemporaryFile(dir=ca_dir, delete=False)
cas_config = """
             [ req ]
             default_bits           = 1024
             distinguished_name     = req_distinguished_name
             prompt                 = no

             [ req_distinguished_name ]
             C                      = {CO}
             ST                     = {ST}
             L                      = {LO}
             O                      = {OG}
             OU                     = {OU}
             CN                     = {CN}
             emailAddress           = {EM}
             """.format(CO="US", ST="North_Carolina", LO="Raleigh", OG="Red_Hat_Inc", OU="Global_Suport_Services", 
                        CN=socket.gethostname(), EM="root@" + socket.gethostname())

config_handle.write(cas_config)
config_handle.close()
#print "REQ Config: {file_name}".format(file_name=config_handle.name)

ca_cert_file_name = ca_dir + os.sep + "ca.pem"
ca_cert_command = "openssl req -new -x509 -key {ca_key_file} -passin pass:{key_pass} -config {config} -out {ca_cert} -days 365 -batch".format(
                  key_pass=CA_key_password, ca_key_file=ca_key_file_name, ca_cert=ca_cert_file_name, config=config_handle.name)

(out, err) = subprocess.Popen(shlex.split(ca_cert_command), stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

CA_config = """
 [ ca ]
 default_ca      = CA_default            # The default ca section
 
 [ CA_default ]
 dir            = {temp_dir}             # top dir
 database       = {db}                  # index file.
 new_certs_dir  = $dir/newcerts         # new certs dir
 
 certificate    = $dir/ca.pem           # The CA cert
 serial         = {serial}              # serial no file
 private_key    = $dir/private/ca.key   # CA private key
 RANDFILE       = {rand}                # random number file
 
 default_days   = 45                    # how long to certify for
 default_crl_days= 30                   # how long before next CRL
 default_md     = md5                   # md to use
 policy         = policy_any            # default policy
 email_in_dn    = no                    # Don't add the email into cert DN
 name_opt       = ca_default            # Subject name display option
 cert_opt       = ca_default            # Certificate display option
 copy_extensions = none                 # Don't copy extensions from request

 [ policy_any ]
 countryName            = supplied
 stateOrProvinceName    = optional
 organizationName       = optional
 organizationalUnitName = optional
 commonName             = supplied
 emailAddress           = optional
            """.format(temp_dir=ca_dir, db=db_handle.name, serial=serial_handle.name, rand=rand_handle.name)

ca_config_handle = tempfile.NamedTemporaryFile(dir=ca_dir, delete=False)
ca_config_handle.write(CA_config)
ca_config_handle.close()
#print "CA Config: {file_name}".format(file_name=ca_config_handle.name)

try:
    cherrypy.server.socket_host = '0.0.0.0'   #socket.gethostbyname(socket.gethostname()) 
    cherrypy.server.socket_port = 8443
    cherrypy.server.ssl_certificate = ca_cert_file_name 
    cherrypy.server.ssl_private_key = ca_key_file_name
except:
    # TODO: LOGGING & Document a Test for this.
    print "Can't determin bind IP based on host name (Not in /etc/hosts)?"    # This Try statement is worthless in its current state.

cherrypy.quickstart(CertBot(working_dir=ca_dir, ca_key=ca_key_file_name, ca_key_pass=CA_key_password, ca_config=ca_config_handle.name))
