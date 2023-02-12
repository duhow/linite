import voluptuous as vol
from dataclasses import dataclass
# TODO semantic version parser lib?

PACKAGE_BINARY_SCHEMA = vol.Schema({
    vol.Required("download"): vol.Url,
    vol.Optional("name"): str,
    vol.Optional("location"): str,
})

PACKAGE_ARCH_SCHEMA = vol.Schema({
    vol.Optional("i386"): str,
    vol.Optional("amd64"): str,
    vol.Optional("arm"): str,
    vol.Optional("arm64"): str,
})

PACKAGE_SCHEMA = vol.Schema({
    vol.Required("name"): str,
    vol.Optional("package"): vol.Url, # package-url
    vol.Required("version"): vol.Coerce(str, ),
    vol.Optional("provides"): str, # executable
    vol.Optional("arch"): PACKAGE_ARCH_SCHEMA,
    vol.Optional("binary"): PACKAGE_BINARY_SCHEMA,
    vol.Optional("check_version"): str,
    vol.Optional("install"): vol.Coerce(str, list),
    vol.Optional("post_install"): vol.Coerce(str, list),
    vol.Optional("requires"): vol.Coerce(str, list) # package deps required
})

@dataclass
class Version:
    # TODO check verion is one of:
    # latest main dev testing rolling
    # if starts with v
    # if is not semver (x.y)
    name: str

    def split(self, index: int) -> str:
        return self.name.split(".")[index]

    @property
    def major(self) -> str:
        return self.split(0)

    @property
    def minor(self) -> str:
        return self.split(1)

    @property
    def patch(self) -> str:
        return self.split(2)

class Package:
    def __init__(self, data: dict):
        PACKAGE_SCHEMA(data)
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        return None

    @property
    def install(self):
        commands = self.data.get("install")
        if isinstance(commands, str):
            commands = commands.split("\n")
        for command in commands:
            # run command
            pass

    @property
    def url(self) -> str:
        # TODO format URL with replacing VERSION and ARCH
        if self.package:
            return self.package
        if self.binary:
            return self.binary.download
        return None

    #def setup(self):
    #    if self.check_version:
    #        # run command and check version first before attempting to setup
    #    if self.requires:
    #        # run apt or dpkg and ensure the listed packages are installed
    #        # otherwise, install them
    #    if self.arch:
    #        # replace ARCH value if any
    #        # eg. amd64 -> x86_64
    #    if self.package:
    #        # download
    #    elif self.binary:
    #        # binary download to path
    #        location = self.binary.location or CONST_DEFAULT_LOCATION
    #        file_name = self.binary.name or self.name
    #    if self.install:
    #        # run setup scripts
    #    if self.post_install:
    #        # run post setup scripts
    #    if self.check_version:
    #        # run command and check version, this also confirms the program is working.
    #        # INSTALLED = True
    #    if self.provides is not None:
    #        if self.provides: # is not empty
    #            # check `command -v` works