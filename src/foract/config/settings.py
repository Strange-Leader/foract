from pydantic import BaseModel

from foract.enums import LogLevel


class ProjectSettings(BaseModel):
    name: str
    version: str
    debug: bool = False


class LoggingSettings(BaseModel):
    level: LogLevel = LogLevel.INFO
    file: str
    console: bool = True


class RegistrySettings(BaseModel):
    auto_discover: bool = True
    plugin_directory: str


class Settings(BaseModel):
    project: ProjectSettings
    logging: LoggingSettings
    registry: RegistrySettings
