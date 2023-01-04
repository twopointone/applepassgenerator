# Standard Library
import decimal
import hashlib
import json
import zipfile
from io import BytesIO

# Third Party Stuff
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7


class Alignment:
    LEFT = "PKTextAlignmentLeft"
    CENTER = "PKTextAlignmentCenter"
    RIGHT = "PKTextAlignmentRight"
    JUSTIFIED = "PKTextAlignmentJustified"
    NATURAL = "PKTextAlignmentNatural"


class BarcodeFormat:
    PDF417 = "PKBarcodeFormatPDF417"
    QR = "PKBarcodeFormatQR"
    AZTEC = "PKBarcodeFormatAztec"
    CODE128 = "PKBarcodeFormatCode128"


class TransitType:
    AIR = "PKTransitTypeAir"
    TRAIN = "PKTransitTypeTrain"
    BUS = "PKTransitTypeBus"
    BOAT = "PKTransitTypeBoat"
    GENERIC = "PKTransitTypeGeneric"


class DateStyle:
    NONE = "PKDateStyleNone"
    SHORT = "PKDateStyleShort"
    MEDIUM = "PKDateStyleMedium"
    LONG = "PKDateStyleLong"
    FULL = "PKDateStyleFull"


class NumberStyle:
    DECIMAL = "PKNumberStyleDecimal"
    PERCENT = "PKNumberStylePercent"
    SCIENTIFIC = "PKNumberStyleScientific"
    SPELLOUT = "PKNumberStyleSpellOut"


class Field(object):
    def __init__(self, key, value, label=""):
        self.key = key  # Required. The key must be unique within the scope
        self.value = value  # Required. Value of the field. For example, 42
        self.label = label  # Optional. Label text for the field.
        self.changeMessage = ""  # Optional. Format string for the alert text that is displayed when the pass is updated
        self.textAlignment = Alignment.LEFT

    def json_dict(self):
        return self.__dict__


class DateField(Field):
    def __init__(
        self,
        key,
        value,
        label="",
        date_style=DateStyle.SHORT,
        time_style=DateStyle.SHORT,
        ignores_time_zone=False,
    ):
        super(DateField, self).__init__(key, value, label)
        self.dateStyle = date_style  # Style of date to display
        self.timeStyle = time_style  # Style of time to display
        self.isRelative = (
            False  # If true, the labels value is displayed as a relative date
        )
        if ignores_time_zone:
            self.ignoresTimeZone = ignores_time_zone

    def json_dict(self):
        return self.__dict__


class NumberField(Field):
    def __init__(self, key, value, label=""):
        super(NumberField, self).__init__(key, value, label)
        self.numberStyle = NumberStyle.DECIMAL  # Style of date to display

    def json_dict(self):
        return self.__dict__


class CurrencyField(NumberField):
    def __init__(self, key, value, label="", currency_code=""):
        super(CurrencyField, self).__init__(key, value, label)
        self.currencyCode = currency_code  # ISO 4217 currency code

    def json_dict(self):
        return self.__dict__


class Barcode(object):
    def __init__(
        self,
        message,
        format=BarcodeFormat.PDF417,
        alt_text="",
        message_encoding="iso-8859-1",
    ):
        self.format = format
        self.message = (
            message  # Required. Message or payload to be displayed as a barcode
        )
        self.messageEncoding = message_encoding  # Required. Text encoding that is used to convert the message
        if alt_text:
            self.altText = alt_text  # Optional. Text displayed near the barcode

    def json_dict(self):
        return self.__dict__


class Location(object):
    def __init__(self, latitude, longitude, altitude=0.0):
        # Required. Latitude, in degrees, of the location.
        try:
            self.latitude = float(latitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
        # Required. Longitude, in degrees, of the location.
        try:
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.longitude = 0.0
        # Optional. Altitude, in meters, of the location.
        try:
            self.altitude = float(altitude)
        except (ValueError, TypeError):
            self.altitude = 0.0
        # Optional. Notification distance
        self.distance = None
        # Optional. Text displayed on the lock screen when
        # the pass is currently near the location
        self.relevantText = ""

    def json_dict(self):
        return self.__dict__


class IBeacon(object):
    def __init__(self, proximity_uuid, major, minor):
        # IBeacon data
        self.proximityUUID = proximity_uuid
        self.major = major
        self.minor = minor

        # Optional. Text message where near the ibeacon
        self.relevantText = ""

    def json_dict(self):
        return self.__dict__


class PassInformation(object):
    def __init__(self):
        self.header_fields = []
        self.primary_fields = []
        self.secondary_fields = []
        self.back_fields = []
        self.auxiliary_fields = []

    def add_header_field(self, key, value, label):
        self.header_fields.append(Field(key, value, label))

    def add_primary_field(self, key, value, label):
        self.primary_fields.append(Field(key, value, label))

    def add_secondary_field(self, key, value, label):
        self.secondary_fields.append(Field(key, value, label))

    def add_back_field(self, key, value, label):
        self.back_fields.append(Field(key, value, label))

    def add_auxiliary_field(self, key, value, label):
        self.auxiliary_fields.append(Field(key, value, label))

    def json_dict(self):
        d = {}
        if self.header_fields:
            d.update({"headerFields": [f.json_dict() for f in self.header_fields]})
        if self.primary_fields:
            d.update({"primaryFields": [f.json_dict() for f in self.primary_fields]})
        if self.secondary_fields:
            d.update(
                {"secondaryFields": [f.json_dict() for f in self.secondary_fields]}
            )
        if self.back_fields:
            d.update({"backFields": [f.json_dict() for f in self.back_fields]})
        if self.auxiliary_fields:
            d.update(
                {"auxiliaryFields": [f.json_dict() for f in self.auxiliary_fields]}
            )
        return d


class BoardingPass(PassInformation):
    def __init__(self, transit_type=TransitType.AIR):
        super(BoardingPass, self).__init__()
        self.transit_type = transit_type
        self.jsonname = "boardingPass"

    def json_dict(self):
        d = super(BoardingPass, self).json_dict()
        d.update({"transitType": self.transit_type})
        return d


class Coupon(PassInformation):
    def __init__(self):
        super(Coupon, self).__init__()
        self.jsonname = "coupon"


class EventTicket(PassInformation):
    def __init__(self):
        super(EventTicket, self).__init__()
        self.jsonname = "eventTicket"


class Generic(PassInformation):
    def __init__(self):
        super(Generic, self).__init__()
        self.jsonname = "generic"


class StoreCard(PassInformation):
    def __init__(self):
        super(StoreCard, self).__init__()
        self.jsonname = "storeCard"


class ApplePass(object):
    def __init__(
        self,
        pass_information,
        json="",
        pass_type_identifier="",
        organization_name="",
        team_identifier="",
    ):

        self._files = {}  # Holds the files to include in the .pkpass
        self._hashes = {}  # Holds the SHAs of the files array

        # Standard Keys

        # Required. Team identifier of the organization that originated and
        # signed the pass, as issued by Apple.
        self.team_identifier = team_identifier
        # Required. Pass type identifier, as issued by Apple. The value must
        # correspond with your signing certificate. Used for grouping.
        self.pass_type_identifier = pass_type_identifier
        # Required. Display name of the organization that originated and
        # signed the pass.
        self.organization_name = organization_name
        # Required. Serial number that uniquely identifies the pass.
        self.serial_number = ""
        # Required. Brief description of the pass, used by the iOS
        # accessibility technologies.
        self.description = ""
        # Required. Version of the file format. The value must be 1.
        self.format_version = 1

        # Visual Appearance Keys
        self.background_color = None  # Optional. Background color of the pass
        self.foreground_color = None  # Optional. Foreground color of the pass,
        self.label_color = None  # Optional. Color of the label text
        self.logo_text = None  # Optional. Text displayed next to the logo
        self.barcode = None  # Optional. Information specific to barcodes. This is deprecated and can only be set to original barcode formats.
        self.barcodes = None  # Optional.  All supported barcodes
        # Optional. If true, the strip image is displayed
        self.suppress_strip_shine = False

        # Web Service Keys

        # Optional. If present, authentication_token must be supplied
        self.web_service_url = None
        # The authentication token to use with the web service
        self.authentication_token = None

        # Relevance Keys

        # Optional. Locations where the pass is relevant.
        # For example, the location of your store.
        self.locations = None
        # Optional. IBeacons data
        self.ibeacons = None
        # Optional. Date and time when the pass becomes relevant
        self.relevant_date = None

        # Optional. A list of iTunes Store item identifiers for
        # the associated apps.
        self.associated_store_identifiers = None
        self.app_launch_url = None
        # Optional. Additional hidden data in json for the passbook
        self.user_info = None

        self.expiration_date = None
        self.voided = None

        self.pass_information = pass_information

    # Adds file to the file array
    def add_file(self, name, fd):
        self._files[name] = fd.read()

    # Creates the actual .pkpass file
    def create(self, certificate, key, wwdr_certificate, password, zip_file=None):
        pass_json = self._create_pass_json()
        manifest = self._create_manifest(pass_json)
        signature = self._create_signature_crypto(
            manifest, certificate, key, wwdr_certificate, password
        )

        if not zip_file:
            zip_file = BytesIO()
        self._create_zip(pass_json, manifest, signature, zip_file=zip_file)
        return zip_file

    def _create_pass_json(self):
        return json.dumps(self, default=pass_handler)

    def _create_manifest(self, pass_json):
        """
        Creates the hashes for all the files included in the pass file.
        """
        self._hashes["pass.json"] = hashlib.sha1(pass_json.encode("utf-8")).hexdigest()
        for filename, filedata in self._files.items():
            self._hashes[filename] = hashlib.sha1(filedata).hexdigest()
        return json.dumps(self._hashes)

    def _read_file_bytes(self, path):
        """
        Utility function to read files as byte data
        :param path: file path
        :returns bytes
        """
        file = open(path)
        return file.read().encode("UTF-8")

    def _create_signature_crypto(
        self, manifest, certificate, key, wwdr_certificate, password
    ):
        """
        Creates a signature (DER encoded) of the manifest.
        Rewritten to use cryptography library instead of M2Crypto
        The manifest is the file
        containing a list of files included in the pass file (and their hashes).
        """
        cert = x509.load_pem_x509_certificate(self._read_file_bytes(certificate))
        priv_key = serialization.load_pem_private_key(
            self._read_file_bytes(key), password=password.encode("UTF-8")
        )
        wwdr_cert = x509.load_pem_x509_certificate(
            self._read_file_bytes(wwdr_certificate)
        )

        options = [pkcs7.PKCS7Options.DetachedSignature]
        return (
            pkcs7.PKCS7SignatureBuilder()
            .set_data(manifest.encode("UTF-8"))
            .add_signer(cert, priv_key, hashes.SHA1())
            .add_certificate(wwdr_cert)
            .sign(serialization.Encoding.DER, options)
        )

    # Creates .pkpass (zip archive)
    def _create_zip(self, pass_json, manifest, signature, zip_file=None):
        zf = zipfile.ZipFile(zip_file or "pass.pkpass", "w")
        zf.writestr("signature", signature)
        zf.writestr("manifest.json", manifest)
        zf.writestr("pass.json", pass_json)
        for filename, filedata in self._files.items():
            zf.writestr(filename, filedata)
        zf.close()

    def json_dict(self):
        d = {
            "description": self.description,
            "formatVersion": self.format_version,
            "organizationName": self.organization_name,
            "passTypeIdentifier": self.pass_type_identifier,
            "serialNumber": self.serial_number,
            "teamIdentifier": self.team_identifier,
            "suppressStripShine": self.suppress_strip_shine,
            self.pass_information.jsonname: self.pass_information.json_dict(),
        }
        # barcodes have 2 fields, 'barcode' is legacy so limit it to the legacy formats, 'barcodes' supports all
        if self.barcode:
            original_formats = [
                BarcodeFormat.PDF417,
                BarcodeFormat.QR,
                BarcodeFormat.AZTEC,
            ]
            legacy_barcode = self.barcode
            new_barcodes = [self.barcode.json_dict()]
            if self.barcode.format not in original_formats:
                legacy_barcode = Barcode(
                    self.barcode.message, BarcodeFormat.PDF417, self.barcode.altText
                )
            d.update({"barcodes": new_barcodes})
            d.update({"barcode": legacy_barcode})

        if self.relevant_date:
            d.update({"relevantDate": self.relevant_date})
        if self.background_color:
            d.update({"backgroundColor": self.background_color})
        if self.foreground_color:
            d.update({"foregroundColor": self.foreground_color})
        if self.label_color:
            d.update({"labelColor": self.label_color})
        if self.logo_text:
            d.update({"logoText": self.logo_text})
        if self.locations:
            d.update({"locations": self.locations})
        if self.ibeacons:
            d.update({"beacons": self.ibeacons})
        if self.user_info:
            d.update({"userInfo": self.user_info})
        if self.associated_store_identifiers:
            d.update({"associatedStoreIdentifiers": self.associated_store_identifiers})
        if self.app_launch_url:
            d.update({"appLaunchURL": self.app_launch_url})
        if self.expiration_date:
            d.update({"expirationDate": self.expiration_date})
        if self.voided:
            d.update({"voided": True})
        if self.web_service_url:
            d.update(
                {
                    "webServiceURL": self.web_service_url,
                    "authenticationToken": self.authentication_token,
                }
            )
        return d


def pass_handler(obj):
    if hasattr(obj, "json_dict"):
        return obj.json_dict()
    else:
        # For Decimal latitude and longitude etc
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return obj
