"""tests.schema"""

from typing import Optional

from pydantic import BaseModel, model_validator


class WriteOperation(BaseModel):
    input: str


class EnterMode(BaseModel):
    requested_mode: str


class SendInputOperation(BaseModel):
    input: str


class SendPromptedInputOperation(BaseModel):
    input: str
    response: str
    prompt_exact: Optional[str] = None
    prompt_pattern: Optional[str] = None

    @model_validator(mode="after")
    def check_prompt_set(self):
        if self.prompt_exact is None and self.prompt_pattern is None:
            raise ValueError("`prompt_exact` or `prompt_pattern` must be set")

        return self


class Operation(BaseModel):
    write: Optional[WriteOperation] = None
    enter_mode: Optional[EnterMode] = None
    send_input: Optional[SendInputOperation] = None
    send_prompted_input: Optional[SendPromptedInputOperation] = None

    @model_validator(mode="after")
    def check_operation_set(self):
        operations = (
            1 if self.write is not None else 0,
            1 if self.enter_mode is not None else 0,
            1 if self.send_input is not None else 0,
            1 if self.send_prompted_input is not None else 0,
        )
        if sum(operations) != 1:
            raise ValueError("exactly one operation must be set")

        return self


class AccessibleMode(BaseModel):
    name: str
    instructions: list[Operation]


class Mode(BaseModel):
    name: str
    prompt_exact: Optional[str] = None
    prompt_pattern: Optional[str] = None
    prompt_excludes: Optional[list[str]] = None
    accessible_modes: Optional[list[AccessibleMode]] = None

    @model_validator(mode="after")
    def check_prompt_set(self):
        if self.prompt_exact is None and self.prompt_pattern is None:
            raise ValueError("`prompt_exact` or `prompt_pattern` must be set")

        return self


class Definition(BaseModel):
    prompt_pattern: str
    default_mode: str
    modes: list[Mode]
    failure_indicators: Optional[list[str]] = None
    on_open_instructions: Optional[list[Operation]] = None
    on_close_instructions: Optional[list[Operation]] = None
    ntc_templates_platform: Optional[str] = None
    genie_platform: Optional[str] = None
