Cert Bot
========
> _Is now standalone: (meaning that it brings with it cherrypy so you dont have to install it as a dependency)_

**Certificate Traning Certificate Authority**

The idea of this project is to explain how an [OpenSSL](http://www.openssl.org/) 
[Certificate Authority](http://www.openssl.org/docs/apps/ca.html#) Works, and 
to convay how to setup an OpenSSL Certificate Authority. 

It is important to note that [OpenSSL](http://www.openssl.org)'s creators never
ment for the CA utility to be used as a full blown CA itself: 

> _"nevertheless some people are using it for this purpose"_

This tool does not attempt to be your organizations CA but it does detail the
full process in creating a certificate, and how a CA signs the certificates.

**Cert Bot** fully written in [Python](http://www.python.org/) and is a 
[CherryPy](http://www.cherrypy.org/) application. Currently these are the only 
two requirements needed to run **Cert Bot**. With the standalone version 
[CherryPy](http://www.cherrypy.org/) is bundled with the application. 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

Copyright (C) 2012 Eric Rich
