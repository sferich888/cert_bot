from django.http import HttpResponse
import socket

def index(request):
    return HttpResponse(
        """
        <h1><a href='/'>{hostname} CertBot</a></h1>
        <p>CertBot is an SSL/TLS training CA, designed to show you how to generate and sign x509 certificates for you PKI infastructure.</p>
        <p>x509 Certificate generation is a three step process for getting a signed Certificate. CertBot gives you the ability to see 
           this process in action as well as quickly generate and test your certificates. 
           <ul>
               <li>The first two steps (links) in the x509 process will direct you through the process of crating an x509 
                   certificate request.</li>
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
    )

def Request_Key(request):
    return HttpResponse(
        """
        <h2><a href='/'>{hostname}</a> Key Request</h2>
        <form action="Requested_Key" method="POST">
        Key Password: <input type="text" name="password" value="password">
        <input type="submit">
        </form>
        <p>The first step in Creating a certificate request is creating a public/private key pair. <br>
           These key are used in the encryption and decryption of data. With x509 certifates or PKI keys 
           these keys can also be used to determin the identity of an entity (known as a signature).</p>
        """.format(hostname=socket.gethostname())
    )

