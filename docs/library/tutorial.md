# Using Apple Wallet Pass

## Create a Pass Client

```python
from applepassgenerator import ApplePassGeneratorClient

TEAM_IDENTIFIER = "<your team id>"
PASS_TYPE_IDENTIFIER = "pass.com.example.mypass"
ORGANIZATION_NAME = "Primedigital Global"

client = ApplePassGeneratorClient(TEAM_IDENTIFIER, PASS_TYPE_IDENTIFIER, ORGANIZATION_NAME)
```

## Create a Card(Pass Layout)

- Create a Card Instance

```python
from applepassgenerator.models import EventTicket, Generic, Coupon, StoreCard, BoardingPass

card0 = EventTicket()
card1 = Generic()
card2 = Coupon()
card3 = StoreCard()
card4 = BoardingPass()
```

- Add Card Details

```python
from applepassgenerator.models import StoreCard

card_info = StoreCard()

card_info.add_primary_field("key", "value", "label")
card_info.add_secondary_field("key", "value", "label")
card_info.add_header_field("key", "value", "label")
card_info.add_auxiliary_field("key", "value", "label")
card_info.add_back_field("key", "value", "label")
```

## Create a Pass Instance

```python
apple_pass = client.get_pass(card_info)
```

- Add Icon, Logo, Strip, Thumbnail to your pass

!!! Note
    Adding `icon.png` and `logo.png` is also mandatory without which a pass will not be created.

```python
apple_pass.addFile("logo.png", open("<path-to-file>/logo.png", "rb"))
apple_pass.addFile("logo@2x.png", open("<path-to-file>/logo@2x.png", "rb"))

apple_pass.addFile("icon.png", open("<path-to-file>/icon.png", "rb"))
apple_pass.addFile("icon@2x.png", open("<path-to-file>/icon@2x.png", "rb"))

apple_pass.addFile("strip.png", open("<path-to-file>/strip.png", "rb"))
apple_pass.addFile("strip@2x.png", open("<path-to-file>/strip@2x.png", "rb"))

apple_pass.addFile("thumbnail.png", open("<path-to-file>/thumbnail.png", "rb"))
apple_pass.addFile("thumbnail@2x.png", open("<path-to-file>/thumbnail@2x.png", "rb"))
```

!!! Note
    Similarly you could add `footer.png` and `background.png` to your pass.

- Adding Barcode to your pass:

```python
from applepassgenerator.models import Barcode

apple_pass.barcode = Barcode(message='Barcode message')
```

- Adding location data to your paas:

```python
from applepassgenerator.models import Location

apple_pass.locations = Location("latitude", "longitude", "altitude")
```
!!! Note
    `latitude` and `longitude` are required fields. Further [reference](https://developer.apple.com/documentation/walletpasses/pass/locations)

- Adding beacons to your pass:

```python
from applepassgenerator.models import IBeacon

apple_pass.ibeacons = IBeacon("proximity_uuid", "major", "minor")
```
!!! Note
    `proximity_uuid` is required. Further [reference](https://developer.apple.com/documentation/walletpasses/pass/beacons)

- Adding Description to your pass:

```python
apple_pass.description = "My Project Pass"
```

- Adding Color to your pass:

```python
apple_pass.foreground_color = "rgb(255, 255, 255)"
apple_pass.background_color = "rgb(255, 110, 0)"
apple_pass.label_color = "rgb(255, 255, 255)"
```

## Checking Pass JSON

Check if your pass is formed correctly before calling `.create()`
```python
apple_pass.json_dict()
```

## Generating a Pass(.pkpass)

```python
CERTIFICATE_PASSWORD = "123456789"

apple_pass.serialNumber = '<some unique identifier>'

apple_pass.create(
        "passes/certificates/certificate.pem",
        "passes/certificates/private.key",
        "passes/certificates/wwdr.pem",
        CERTIFICATE_PASSWORD,
        "passes/mypass.pkpass",
    )
```
!!! Note
    `serialNumber` will be used to uniquely identify a pass and is a mandatory field for creating a pass.
