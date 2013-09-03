isdhcplib
=========

**Description:** Pure python DHCP library.

**Build status:** |travis-ci|


Origin
------
Based on pydhcplib by Mathieu Ignacio (http://pydhcplib.tuxfamily.org)

Features
--------
isdhcplib can **read and write dhcp packet** on network

You can choose **port** on which you want to read or write

Can **encode and decode dhcp** packet

Added support for **option 82**. It mostly used for customer authorizations and so on.


Debian packaging
----------------
To build .deb package run

dpkg-buildpackage -b


.. |travis-ci| image:: https://travis-ci.org/ialx/isdhcplib.png
