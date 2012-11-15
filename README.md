Cert Bot
========

Certificate Training Certificate Authority 

The idea of this project is to explain how an [OpenSSL](http://www.openssl.org/) 
[Certificate Authority](http://www.openssl.org/docs/apps/ca.html#) Works, and 
to convay how to setup an OpenSSL Certificate Authority. 

It is important to note that [OpenSSL](http://www.openssl.org)'s creators never
ment for the CA utility to be used as a full blown CA itself: 

_"nevertheless some people are using it for this purpose"_

This tool does not attempt to be your organizations CA but it does detail the
full process in creating a certificate, and how a CA signs the certificates.

**Cert Bot** fully written in [Python](http://www.python.org/) and is a 
[CherryPy](http://www.cherrypy.org/) application. Currently these are the only 
two requirements needed to run **Cert Bot**. 
