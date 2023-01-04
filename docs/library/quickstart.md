# Quickstart

Here is some code to quickly get you started:

```python
from applepassgenerator import ApplePassGeneratorClient
from applepassgenerator.models import EventTicket

card_info = EventTicket()
card_info.add_primary_field('name', 'Tony Stark', 'Name')
card_info.add_secondary_field('loc', 'USA', 'Country')

applepassgenerator_client = ApplePassGeneratorClient(pass_type_identifier="pass.com.project.example",
                                                       organization_name="PrimeDigital Global",
                                                       team_identifier="<Team Identifier>")
apple_pass = applepassgenerator_client.get_pass(card_info)

# Add logo/icon/strip image to file
apple_pass.add_file("logo.png", open("<path-to-file>/logo.png", "rb"))
apple_pass.add_file("icon.png", open("<path-to-file>/icon.png", "rb"))

CERTIFICATE_PATH = '<path>/certificate.pem'
PASSWORD_KEY = '<path>/password.key'
WWDR_PATH = '<path>/wwdr.pem'
CERTIFICATE_PASSWORD = "<password>"
OUTPUT_PASS_NAME = "mypass.pkpass"

# Creates a .pkpass file
apple_pass.create(CERTIFICATE_PATH, PASSWORD_KEY, WWDR_PATH, CERTIFICATE_PASSWORD, OUTPUT_PASS_NAME)
```
