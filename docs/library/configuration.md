# Configuration

To start using the lib, some Apple files are needed, as well as some action in order to convert them to more friendly formats:

### 1. Get Pass Type ID

- Go to the [Apple Developer page ➵ Identifiers ➵ Pass Type IDs](https://developer.apple.com/account/ios/identifiers/passTypeId/passTypeIdList.action).
- Next, you need to create a pass type ID. This is similar to the bundle ID for apps. It will uniquely identify a specific kind of pass. It should be of the form of a reverse-domain name style string (i.e., pass.com.example.appname).

### 2. Generate the necessary certificate

- After creating the pass type ID, click on Edit and follow the instructions to create a new Certificate.
- Once the process is finished, the pass certificate can be downloaded. That's not it though, the certificate is downloaded as `.cer` file, which need to be converted to `.p12` in order to work. If you are using a Mac you can import it into Keychain Access and export it as `.p12`from there.
- if now you have `certificate.p12` file follow the steps below to convert it to `certifictate.pem`

```markdown
$ openssl pkcs12 -in certificate.p12 -clcerts -nokeys -out certificate.pem
```

### 3. Generate the key.pem

```markdown
>$ openssl pkcs12 -in certificate.p12 -nocerts -out private.key
```

!!! Note
    while generating this `private.key` file you will be asked for a PEM pass phrase which will be used as the `CERTIFICATE_PASSWORD` attribute throughout the Package.

### 4. Getting WWDR Certificate

- If you have made iOS development, you probably have already the Apple Worldwide Developer Relations Intermediate Certificate in your Mac’s keychain.
- If not, it can be downloaded from the [Apple Website](https://www.apple.com/certificateauthority/) (on `.cer` format). This one needs to be exported as `.pem`, It can be exported from KeyChain into a `.pem` (e.g. wwdr.pem).
