"""工具函数"""

import re


def to_snake_case(text: str) -> str:
    """maintenanceMode -> maintenance_mode"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case(text: str) -> str:
    """maintenance_mode -> maintenanceMode"""
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

