from __future__ import absolute_import
from builtins import map
from builtins import object
from . import utils

class Organization(object):
    def __init__(self, id=None, created_on=None, updated_on=None, name=None, email=None, timezone=None, country=None, delegatee_ids=None, image=None):
        self.id = id
        self.created_on = created_on
        self.updated_on = updated_on
        self.name = name
        self.email = email
        self.timezone = timezone
        self.country = country
        self.delegatee_ids = delegatee_ids
        self.image = image

    def __repr__(self):
        return "<Organization id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        return Organization(
            id=obj['id'],
            created_on=obj['timeCreated'],
            updated_on=obj['timeLastModified'],
            name=obj['name'],
            email=obj['email'],
            delegatee_ids=obj['delegatees'],
            image=obj['image'],
            country=obj['country']
        )


class Administrator(object):
    def __init__(self, name, email, phone=None, id=None, user_type=None, organization_id=None, active=None, created_on=None, updated_on=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.id = id
        self.user_type = user_type
        self.organization_id = organization_id
        self.active = active
        self.created_on = created_on
        self.updated_on = updated_on

    def __repr__(self):
        return "<Administrator id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        admin = Administrator(
            name=obj['name'],
            email=obj['email'],
            id=obj['id'],
            created_on=obj['timeCreated'],
            updated_on=obj['timeLastModified'],
            active=obj['isActive'],
            user_type=obj['type'],
            organization_id=obj['organization'],
        )

        admin.phone = obj.get('phone')
        return admin


class Recipient(object):
    def __init__(self, name, phone, notes=None, created_on=None, updated_on=None, id=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.notes = notes
        self.created_on = created_on
        self.updated_on = updated_on

    def __repr__(self):
        return "<Recipient id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        recipient = Recipient(
            id=obj['id'],
            created_on=obj['timeCreated'],
            updated_on=obj['timeLastModified'],
            name=obj['name'],
            phone=obj['phone'],
            notes=obj['notes']
        )

        return recipient


class Task(object):
    UNASSIGNED = 0
    ASSIGNED = 1
    ACTIVE = 2
    COMPLETED = 3

    def __init__(self, destination, recipients, notes=None, state=None,
            id=None, created_on=None, updated_on=None, merchant=None,
            executor=None, pickup_task=False, tracking_url=None,
            dependencies=None, complete_after=None, complete_before=None):
        self.id = id
        self.created_on = created_on
        self.updated_on = updated_on
        self.merchant = merchant
        self.executor = executor
        self.destination = destination
        self.recipients = recipients
        self.notes = notes
        self.pickup_task = pickup_task
        self.tracking_url = tracking_url
        self.complete_after = complete_after
        self.complete_before = complete_before
        self.dependencies = dependencies

    def __repr__(self):
        return "<Task id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        task = Task(
            id=obj['id'],
            created_on=obj['timeCreated'],
            updated_on=obj['timeLastModified'],
            state=obj['state'],
            notes=obj['notes'],
            destination=Destination.parse(obj['destination']),
            recipients=list(map(Recipient.parse, obj['recipients'])),
            pickup_task=obj['pickupTask'],
            tracking_url=obj['trackingURL'],
            complete_after=obj['completeAfter'],
            complete_before=obj['completeBefore'],
            dependencies=obj['dependencies'],
        )
        if obj['completeAfter']:
            task.complete_after = utils.from_unix_time(obj['completeAfter'])

        if obj['completeBefore']:
            task.complete_before = utils.from_unix_time(obj['completeBefore'])

        if 'worker' in obj and obj['worker'] is not None:
            task.worker = obj['worker']

        return task


class Address(object):
    def __init__(self, street=None, number=None, city=None, country=None, name=None, apartment=None, state=None, postal_code=None, unparsed=None):
        self.street = street
        self.number = number
        self.city = city
        self.country = country
        self.name = name
        self.apartment = apartment
        self.state = state
        self.postal_code = postal_code
        self.unparsed = unparsed

    def __repr__(self):
        return "<Address street='{}'>".format(self.street)

    @classmethod
    def parse(self, obj):
        address = Address(
            apartment=obj['apartment'],
            state=obj['state'],
            postal_code=obj['postalCode'],
            country=obj['country'],
            city=obj['city'],
            street=obj['street'],
            number=obj['number']
        )
        return address


class Destination(object):
    def __init__(self, address=None, location=None, notes=None, id=None, created_on=None, updated_on=None, tasks=None):
        self.id = id
        self.address = address
        self.location = location
        self.notes = notes

    def __repr__(self):
        return "<Destination id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        destination = Destination(
            id=obj['id'],
            created_on=obj['timeCreated'],
            updated_on=obj['timeLastModified'],
            location=obj['location'],
            address=Address.parse(obj['address']),
            notes=obj['notes'],
        )

        if 'tasks' in obj:
            destination.tasks = obj['tasks']

        return destination


class Vehicle(object):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    BICYCLE = "BICYCLE"
    TRUCK = "TRUCK"


    def __init__(self, vehicle_type, description=None, license_plate=None, color=None, id=None):
        if vehicle_type not in [Vehicle.CAR, Vehicle.MOTORCYCLE, Vehicle.BICYCLE, Vehicle.TRUCK]:
            raise Exception

        self.id = id
        self.vehicle_type = vehicle_type
        self.description = description
        self.license_plate = license_plate
        self.color = color

    def __repr__(self):
        return "<Vehicle id='{}'>".format(self.id)

    @classmethod
    def parse(self, obj):
        vehicle = Vehicle(
            id=obj['id'],
            vehicle_type=obj['type'],
        )

        if 'description' in obj:
            vehicle.team_ids = obj['description']

        if 'license_plate' in obj:
            vehicle.team_ids = obj['licensePlate']

        if 'color' in obj:
            vehicle.team_ids = obj['color']

        return vehicle


class Worker(object):
    def __init__(self, name=None, phone=None, team_ids=None, vehicle=None, id=None, tasks=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.team_ids = team_ids
        self.vehicle = vehicle
        self.tasks = tasks

    def __repr__(self):
        return "<Worker name='{}'>".format(self.name)

    @classmethod
    def parse(self, obj):
        worker = Worker(
            id=obj['id'],
            name=obj['name'],
            phone=obj['phone'],
            vehicle=Vehicle.parse(obj['vehicle'])
        )

        if 'teams' in obj:
            worker.team_ids = obj['teams']

        return worker

