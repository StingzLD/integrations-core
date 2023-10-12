# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.dev.utils import get_metadata_metrics

from .. import common
from ..test_e2e_core_metadata import assert_device_metadata
from .utils import (
    assert_all_profile_metrics_and_tags_covered,
    assert_common_metrics,
    assert_extend_generic_if,
    create_e2e_core_test_config,
    get_device_ip_from_config,
)

pytestmark = [pytest.mark.e2e, common.py3_plus_only, common.snmp_integration_only]


def test_e2e_features(dd_agent_check):
    profile = 'features'
    config = create_e2e_core_test_config(profile)
    aggregator = common.dd_agent_check_wrapper(dd_agent_check, config, rate=True)

    ip_address = get_device_ip_from_config(config)
    common_tags = [
        'snmp_profile:features',
        'snmp_host:features.device.name',
        'device_namespace:default',
        'snmp_device:' + ip_address,
    ]

    # --- TEST EXTENDED METRICS ---

    # --- TEST METRICS ---
    assert_common_metrics(aggregator, common_tags)

    tag_rows = [
        [
            'tag_using_deprecated_column_syntax:If1',
            'interface_alias:If1Alias',
        ],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.ifInErrors', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    # --- TEST METADATA ---
    device = {
        'description': 'Fake features test device',
        'id': 'default:' + ip_address,
        'id_tags': ['device_namespace:default', 'snmp_device:' + ip_address],
        'ip_address': '' + ip_address,
        'name': 'features.device.name',
        'profile': 'features',
        'status': 1,
        'sys_object_id': '1.2.3.20231012'
    }
    device['tags'] = common_tags
    assert_device_metadata(aggregator, device)

    # --- CHECK COVERAGE ---
    aggregator.assert_all_metrics_covered()
