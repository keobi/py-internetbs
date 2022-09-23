from marshmallow import Schema, EXCLUDE, fields
from .fields import *


__all__ = [
    "ContactSchema", "DomainSchema", "DomainsSchema", "DomainContactListSchema",
]


class ContactSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    first_name = fields.Str(
        data_key="firstname"
    )
    last_name = fields.Str(
        data_key="lastname"
    )
    email = fields.Email()
    phone = fields.Str(
        data_key="phonenumber"
    )
    company = fields.Str(
        data_key="organization"
    )
    address_line1 = fields.Str(
        data_key="street"
    )
    address_line2 = fields.Str(
        data_key="street2"
    )
    address_city = fields.Str(
        data_key="city"
    )
    address_state = fields.Str(
        data_key="state"
    )
    address_postalcode = fields.Str(
        data_key="postalcode"
    )
    address_country = fields.Str(
        data_key="countrycode"
    )


class DomainContactListSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    technical = fields.Nested(
        ContactSchema()
    )
    billing = fields.Nested(
        ContactSchema()
    )
    registrant = fields.Nested(
        ContactSchema()
    )
    admin = fields.Nested(
        ContactSchema()
    )


class DomainSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    domain = fields.Str()
    expiration_date = fields.Date(
        data_key="expirationdate",
        format="%Y/%m/%d"
    )
    registration_date = fields.Date(
        data_key="registrationdate",
        format="%Y/%m/%d"
    )
    paid_through_date = fields.Date(
        data_key="paiduntil",
        format="%Y/%m/%d"
    )
    status = SpecialBoolField(
        true_value="success",
        false_value="failure",
        upper=True
    )
    is_auto_renewed = YesNoBoolField(
        upper=True,
        data_key="autorenew"
    )
    transfer_auth_info = fields.Str(
        data_key="transferauthinfo",
    )
    registrar_lock_status = SpecialBoolField(
        true_value="enabled",
        false_value=["disabled", "notadmitted"],
        upper=True
    )
    contacts = fields.Nested(DomainContactListSchema())
    nameservers = fields.List(
        fields.Str(),
        data_key="nameserver"
    )


class DomainsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    count = fields.Int(
        data_key="domaincount"
    )
    domains = fields.List(
        fields.Str(),
        data_key="domain"
    )
