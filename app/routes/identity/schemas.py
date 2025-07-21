from pydantic import Field, field_validator, model_validator
from typing import Annotated
from fastapi import HTTPException
from app.base_schema import BaseSchema

class Domain(BaseSchema):
    id: str | None = None
    name: str | None = None

    @model_validator(mode='after')
    def validate_id_and_name(self):
        if not self.id and not self.name:
            raise ValueError("Domain id or name cannot be empty.")
        return self

class Project(BaseSchema):
    id: str | None = None
    name: str | None = None
    domain: Domain | None = None

    @model_validator(mode='after')
    def validate_id_and_name(self):
        if not self.id and not self.name:
            raise ValueError("Project id or name cannot be empty.")
        return self

    @model_validator(mode='after')
    def validate_name_and_domain(self):
        if self.name and not self.domain:
            raise ValueError("Domain must be provided if using project name")
        return self

class Token(BaseSchema):
    id: str

class User(BaseSchema):
    id: str | None = None
    name: str | None = None
    password: str
    domain: Domain | None = None

    @model_validator(mode='after')
    def validate_id_name(self):
        if not self.id and not self.name:
            raise ValueError("User name or id cannot be empty.")
        return self

class Password(BaseSchema):
    user: User

class Identity(BaseSchema):
    methods: list[str]
    password: Password | None = None
    token: Token | None = None

    @model_validator(mode='after')
    def validate_methods(self):
        if not self.methods:
            raise ValueError("At least one authentication method must be provided.")
        if 'password' in self.methods and not self.password:
            raise ValueError("Password authentication method is required.")
        if 'token' in self.methods and not self.token:
            raise ValueError("Token authentication method requires a token object.")
        return self

class Scope(BaseSchema):
    project: Project | None = None
    domain: Domain | None = None

    @model_validator(mode='after')
    def validate_project(self):
        if not self.project and not self.domain:
            raise ValueError("Scope requires either a project or a domain.")
        return self

class AuthRequest(BaseSchema):
    identity: Identity
    scope: Scope | None = None
