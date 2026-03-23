"""tests.schema"""

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
    prompt_exact: str | None = None
    prompt_pattern: str | None = None

    @model_validator(mode="after")
    def check_prompt_set(self):
        if self.prompt_exact is None and self.prompt_pattern is None:
            raise ValueError("`prompt_exact` or `prompt_pattern` must be set")

        return self


class Operation(BaseModel):
    write: WriteOperation | None = None
    enter_mode: EnterMode | None = None
    send_input: SendInputOperation | None = None
    send_prompted_input: SendPromptedInputOperation | None = None

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
    prompt_exact: str | None = None
    prompt_pattern: str | None = None
    prompt_excludes: list[str] | None = None
    accessible_modes: list[AccessibleMode] | None = None

    @model_validator(mode="after")
    def check_prompt_set(self):
        if self.prompt_exact is None and self.prompt_pattern is None:
            raise ValueError("`prompt_exact` or `prompt_pattern` must be set")

        return self


class Definition(BaseModel):
    prompt_pattern: str
    default_mode: str
    modes: list[Mode]
    failure_indicators: list[str] | None = None
    on_open_instructions: list[Operation] | None = None
    on_close_instructions: list[Operation] | None = None
    force_in_session_auth: bool | None = None
    bypass_in_session_auth: bool | None = None
    ntc_templates_platform: str | None = None
    genie_platform: str | None = None
