# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from pydantic import BaseModel, Field, root_validator, validator

from datadog_checks.base.utils.functions import identity
from datadog_checks.base.utils.models import validation

from . import defaults, validators


class MetricPatterns(BaseModel):
    class Config:
        allow_mutation = False

    exclude: Optional[Sequence[str]]
    include: Optional[Sequence[str]]


class InstanceConfig(BaseModel):
    class Config:
        allow_mutation = False

    auto_discover_channels: Optional[bool]
    auto_discover_queues: Optional[bool]
    channel: str = Field(..., min_length=1)
    channel_status_mapping: Optional[Mapping[str, Any]]
    channels: Optional[Sequence[str]]
    collect_reset_queue_metrics: Optional[bool]
    collect_statistics_metrics: Optional[bool]
    connection_name: Optional[str] = Field(None, min_length=1)
    convert_endianness: Optional[bool]
    disable_generic_tags: Optional[bool]
    empty_default_hostname: Optional[bool]
    host: Optional[str] = Field(None, min_length=1)
    metric_patterns: Optional[MetricPatterns]
    min_collection_interval: Optional[float]
    mqcd_version: Optional[float] = Field(None, ge=1.0)
    override_hostname: Optional[bool]
    password: Optional[str] = Field(None, min_length=1)
    port: Optional[int]
    queue_manager: str = Field(..., min_length=1)
    queue_manager_timezone: Optional[str] = Field(None, min_length=1)
    queue_patterns: Optional[Sequence[str]]
    queue_regex: Optional[Sequence[str]]
    queue_tag_re: Optional[Mapping[str, Any]]
    queues: Optional[Sequence[str]]
    service: Optional[str]
    ssl_auth: Optional[bool]
    ssl_certificate_label: Optional[str]
    ssl_cipher_spec: Optional[str]
    ssl_key_repository_location: Optional[str] = Field(None, min_length=1)
    tags: Optional[Sequence[str]]
    timeout: Optional[int]
    try_basic_auth: Optional[bool]
    username: Optional[str] = Field(None, min_length=1)

    @root_validator(pre=True)
    def _initial_validation(cls, values):
        return validation.core.initialize_config(getattr(validators, 'initialize_instance', identity)(values))

    @validator('*', pre=True, always=True)
    def _ensure_defaults(cls, v, field):
        if v is not None or field.required:
            return v

        return getattr(defaults, f'instance_{field.name}')(field, v)

    @validator('*')
    def _run_validations(cls, v, field):
        if not v:
            return v

        return getattr(validators, f'instance_{field.name}', identity)(v, field=field)

    @root_validator(pre=False)
    def _final_validation(cls, values):
        return validation.core.finalize_config(getattr(validators, 'finalize_instance', identity)(values))
