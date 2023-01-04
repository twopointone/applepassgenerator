# Apple Pass Generator

Python library to generate passes i.e (.pkpass) files compatible with Apple Wallet (former Passbook).

## Table of Contents

- [💾 Installation](#-installation)
- [🍎 Apple docs](#-apple-docs)
- [📝 Configuration](#-configuration)
- [🚀 Usage](#-usage)
- [📜 Code Of Conduct](#code-of-conduct)

### 💾 Installation

To easily install or upgrade to the latest release, use pip.

```
$ pip install applepassgenerator
```

### 🍎 Apple docs

From now on, some stuff is much better explained on the Apple docs, so when in doubt just check (if you haven't done so) the following documents:

- [Wallet Portal](https://developer.apple.com/wallet/)
- [Wallet Developer Guide](https://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/PassKit_PG/index.html#//apple_ref/doc/uid/TP40012195)
- [Crypto Signatures](https://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html#//apple_ref/doc/uid/TP40012195-CH4-SW55)
- [PassKit Package Format Reference](https://developer.apple.com/library/ios/documentation/UserExperience/Reference/PassKit_Bundle/Chapters/Introduction.html#//apple_ref/doc/uid/TP40012026)

### 📝 Configuration

To start using the lib, some Apple files are needed, as well as some action in order to convert them to more friendly formats:

- Get Pass Type ID
    - Go to the [Apple Developer page ➵ Identifiers ➵ Pass Type IDs](https://developer.apple.com/account/ios/identifiers/passTypeId/passTypeIdList.action).
    - Next, you need to create a pass type ID. This is similar to the bundle ID for apps. It will uniquely identify a specific kind of pass. It should be of the form of a reverse-domain name style string (i.e., pass.com.example.appname).

- Generate the necessary certificate
    - After creating the pass type ID, click on Edit and follow the instructions to create a new Certificate.
    - Once the process is finished, the pass certificate can be downloaded. That's not it though, the certificate is downloaded as `.cer` file, which need to be converted to `.p12` in order to work. If you are using a Mac you can import it into Keychain Access and export it as `.p12`from there.
    - if now you have `certificate.p12` file follow the steps below to convert it to `certifictate.pem`

        ```markdown
        $ openssl pkcs12 -in certificate.p12 -clcerts -nokeys -out certificate.pem
        ```

- Generate the key.pem

    ```markdown
    >$ openssl pkcs12 -in certificate.p12 -nocerts -out private.key
    ```

    Note: While generating this `private.key` file you will be asked for a PEM pass phrase which will be used as the `CERTIFICATE_PASSWORD` attribute throughout the Package.

- Getting WWDR Certificate

    - If you have made iOS development, you probably have already the Apple Worldwide Developer Relations Intermediate Certificate in your Mac’s keychain.
    - If not, it can be downloaded from the [Apple Website](https://www.apple.com/certificateauthority/) (on `.cer` format). This one needs to be exported as `.pem`, It can be exported from KeyChain into a `.pem` (e.g. wwdr.pem).

### 🚀 Usage

```python
from applepassgenerator import ApplePassGeneratorClient
from applepassgenerator.models import EventTicket

card_info = EventTicket()
card_info.add_primary_field('name', 'Tony Stark', 'Name')
card_info.add_secondary_field('loc', 'USA', 'Country')

team_identifier = "1234ABCDEF"
pass_type_identifier = "pass.com.project.example"
organization_name = "Primedigital Global"

applepassgenerator_client = ApplePassGeneratorClient(team_identifier, pass_type_identifier, organization_name)
apple_pass = applepassgenerator_client.get_pass(card_info)

# Add logo/icon/strip image to file
apple_pass.add_file("logo.png", open("<path>/logo.png", "rb"))
apple_pass.add_file("icon.png", open("<path>/icon.png", "rb"))

CERTIFICATE_PATH = "<path-to-file>/certificate.pem"
PASSWORD_KEY = "<path-to-file>/password.key"
WWDR_CERTIFICATE_PATH = "<path-to-file>/wwdr.pem"
CERTIFICATE_PASSWORD = "<password>"
OUTPUT_PASS_NAME = "mypass.pkpass"

apple_pass.create(CERTIFICATE_PATH, PASSWORD_KEY, WWDR_CERTIFICATE_PATH, CERTIFICATE_PASSWORD, OUTPUT_PASS_NAME)
```

### Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, we have a code of conduct, which can be found [here](CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python and Apple Pass Generator with you.
