Python-Onfleet
==============

|ci|_   |version|_   |downloads|_

.. |ci| image:: https://img.shields.io/travis/lionheart/python-onfleet.svg?style=flat
.. _ci: https://travis-ci.org/lionheart/onfleet.py

.. |downloads| image:: https://img.shields.io/pypi/dm/onfleet.svg?style=flat
.. _downloads: https://pypi.python.org/pypi/onfleet

.. |version| image:: https://img.shields.io/pypi/v/onfleet.svg?style=flat
.. _version: https://pypi.python.org/pypi/onfleet

python-onfleet is an easy-to-use and fully-functional Python wrapper for the `Onfleet API <http://docs.onfleet.com/v2.0/>`_.

Installation
------------

python-onfleet is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

   pip install onfleet

No dependencies (besides Python >= 2.7).

Usage
-----

To get started, you're going to need to get an Onfleet account set up and create an API token. Once you've got that, you're ready to go.

.. code:: pycon

   >>> import onfleet
   >>> on = onfleet.Onfleet(api_token)

Once you've done this, you can now use the `on` object to make calls to the Onfleet API. Here are some examples:

Organizations
'''''''''''''

.. code:: pycon

   >>> organization = on.organization()
   >>> organization
   <Organization id='O1o6D8OryDMILx2YEW3YOFFg'>
   >>> organization.created_on
   1425052175000


Administrators
''''''''''''''

Create a new administrator:

.. code:: pycon

   >>> administrator = onfleet.Administrator(name="John Doe", email="john@example.com")
   >>> on.admins(administrator, method="POST")
   <Administrator id='lMmclZVdpCqzpN9~tSzvIjHn'>

List all administrators:

.. code:: pycon

   >>> on.admins()
   [<Administrator id='lMmclZVdpCqzpN9~tSzvIjHn'>,
    <Administrator id='IP4mhhsuA*RivOvpJG9y~tI7'>]
   >>> admins = _
   >>> admins[0].name
   John Doe

Workers
'''''''

List workers:

.. code:: pycon

   >>> on.workers()
   <Worker name='John D'>, <Worker name='Sally D'>]

Create a new worker:

.. code:: pycon

   >>> vehicle = onfleet.Vehicle(vehicle_type=onfleet.Vehicle.CAR, description="2010 Jetta", licensePlate="123456", color="White")
   >>> worker = onfleet.Worker(name="John Smith", phone="1234567890", vehicle=vehicle)
   >>> on.worker(worker, method="POST")

Get a single worker:

.. code:: pycon

   >>> onfleet.Worker[worker_id]()
   <Worker name='John D'>

Update a worker:

.. code:: pycon

   >>> worker = onfleet.Worker(id="12345", tasks=["1234"])
   >>> on.worker(worker, method="PUT")

Teams
'''''

List teams:

.. code:: pycon

   >>> on.teams()
   [{u'id': u'n3MMWj0Cq6emWBg1v0ugJ46f',
     u'managers': [u'BKH3rtJxU*XdH6anWsn1YEsU'],
     u'name': u'Test Team',
     u'timeCreated': 1427748462000,
     u'timeLastModified': 1427905261933,
     u'workers': [u'i0TlEqfEk8E65a4dW~0J58VZ', u'SKmm09tPTCLkEWnGKW1AsLh9']}]

Get a single team:

.. code:: pycon

   >>> on.teams['n3MMWj0Cq6emWBg1v0ugJ46f']()
   {u'id': u'n3MMWj0Cq6emWBF1a0ugJ46f',
    u'managers': [],
    u'name': u'Test Team',
    u'timeCreated': 1427748462000,
    u'timeLastModified': 1427905261933,
    u'workers': [{u'id': u'i0TlEqfak8E65i4dW~0J58VZ',
      u'name': u'John D',
      u'phone': u'+17172372831'},
     {u'id': u'SKmm09j3jJJKHanGKW1AsLW9',
      u'name': u'Sally R',
      u'phone': u'+15023838282'}]}

Destinations
''''''''''''

Create a new destination:

.. code:: pycon

   >>> destination = on.destinations(Destination(address=Address(unparsed="543 Howard Street, San Francisco, CA 94105")), method="POST")
   >>> destination
   <Destination id='RJ6SnbJntnGx3M72QvDnWDhn'>
   >>> destination.location
   [-122.3965731, 37.7875728]


Get a single destination:

.. code:: pycon

   >>> on.destinations['RJ6SnbJntnGx3M72QvDnWDhn']()
   <Destination id='RJ6SnbJntnGx3M72QvDnWDhn'>


Tasks
'''''

TODO

Recipients
''''''''''

TODO

Miscellaneous
'''''''''''''

By default, python-onfleet will return parsed JSON objects. If you'd like the raw response object for a request, just pass in `parse_response=False`.

.. code:: pycon

   >>> response = on.organization(parse_response=False)
   ... your org ...


Python-onfleet maps 1-1 to the Onfleet API (e.g., pb.one.two.three['1234']() will send a request to "https://api.onfleet.com/api/v2/one/two/three/1234"). For more information on other methods and usage, please read the `Onfleet API documentation <http://docs.onfleet.com/v2.0/docs>`_.

Support
-------

If you like this library, or need help implementing it, send us an email: hi@lionheartsw.com.

License
-------

.. image:: http://img.shields.io/pypi/l/onfleet.svg?style=flat
   :target: LICENSE

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.

