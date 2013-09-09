isdhcplib
=========

**Description:** Pure python DHCP library.

**Build status:** |travis-ci|


Origin
------
Based on pydhcplib by Mathieu Ignacio (http://pydhcplib.tuxfamily.org)


Features
--------
isdhcplib can decode & encode DHCP packet (RFC 2131). It can be used to develop 
monitoring & diagnostic tools or event to build fully functional DHCP server.
Library support most of dhcp options (including options 82,121,249).


Debian packaging
----------------
To build .deb package run

dpkg-buildpackage -b


.. |travis-ci| image:: https://travis-ci.org/ialx/isdhcplib.png
