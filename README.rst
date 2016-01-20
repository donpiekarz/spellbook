=========
spellbook
=========

store and search command lines

-------
problem
-------

.. image:: http://imgs.xkcd.com/comics/tar.png




The inspiration is user experience in opennssl command line tool.
In one of my previous project I was working with openssl command line tool.
In the examples below I will use openssl to show you how to use spellbook.

get started
===========


The idea is to create 'book' for openssl.

install spellbook:

.. code::

    $ pip install spellbook

create your first spellbook, called openssl:

.. code:: 

    $ spellbook openssl create

then create spellbook for linux:

.. code:: 

    $ spellbook linux create


add
---

add some data to it, three ways are possible:

format:

.. code:: 

    $ spellbook <book_name> add [command [description]]

add with command and description:

.. code:: 

    $ spellbook openssl add "openssl rand 16 -hex" "generate random 16 bytes and encode as hex"
    openssl rand 16 -hex::generate random 16 bytes and encode as hex

add with only command:

.. code:: 

    $ spellbook openssl add "openssl asn1parse -in 3msg.enc.der -inform der"
    provide description>> show asn1 encoded file
    openssl asn1parse -in 3msg.enc.der -inform der::show asn1 encoded file

add without command:

.. code:: 

    $ spellbook openssl add
    provide command>> openssl des3 -d -in 3msg.enc.msg -K `xxd -p 3msg.dec.key` -iv `xxd -p 3msg.iv`
    provide description>> decode file using des3 with key and iv
    openssl des3 -d -in 3msg.enc.msg -K `xxd -p 3msg.dec.key` -iv `xxd -p 3msg.iv`::decode file using des3 with key and iv

add something to linux book:

.. code:: 

    $ spellbook linux add "tar -xvzf file.tar.gz" "extract tar.gz archive"
    tar -xvzf file.tar.gz::extract tar.gz archive


search
------

search in book openssl:

.. code:: 

    $ spellbook openssl search rand
    openssl rand 16 -hex

or in all books ( - means all ):

.. code:: 

    $ spellbook - search extract
    tar -xvzf file.tar.gz

search any word:

.. code:: 

    $ spellbook - search openssl d
    openssl rand 16 -hex
    openssl asn1parse -in 3msg.enc.der -inform der
    openssl des3 -d -in 3msg.enc.msg -K `xxd -p 3msg.dec.key` -iv `xxd -p 3msg.iv`

or full pharse:

.. code:: 

    $ spellbook - search "openssl d"
    openssl des3 -d -in 3msg.enc.msg -K `xxd -p 3msg.dec.key` -iv `xxd -p 3msg.iv`


list
----

list all spells:

.. code:: 

    $ spellbook openssl list
    openssl rand 16 -hex    ::>>    generate random 16 bytes and encode as hex
    openssl asn1parse -in 3msg.enc.der -inform der  ::>>    show asn1 encoded file
    openssl des3 -d -in 3msg.enc.msg -K `xxd -p 3msg.dec.key` -iv `xxd -p 3msg.iv`  ::>>    decode file using des3 with key and iv


future work
===========

* builtin support for github repositories to store all spellbooks
* some hack to end parse arguments


