"""Patch dbt base_types.py to handle protobuf version mismatch."""

target = "/opt/dbt-venv/lib/python3.11/site-packages/dbt_common/events/base_types.py"

with open(target, "r") as f:
    content = f.read()

# Patch to_json method
content = content.replace(
    """    def to_json(self) -> str:
        return MessageToJson(
            self.pb_msg,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
            indent=None,
            sort_keys=True,
        )""",
    """    def to_json(self) -> str:
        try:
            return MessageToJson(
                self.pb_msg,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True,
                indent=None,
                sort_keys=True,
            )
        except TypeError:
            return MessageToJson(
                self.pb_msg,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
                indent=None,
                sort_keys=True,
            )""",
)

# Patch to_dict method too
content = content.replace(
    """        return MessageToDict(
            self.pb_msg,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )""",
    """        try:
            return MessageToDict(
                self.pb_msg,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True,
            )
        except TypeError:
            return MessageToDict(
                self.pb_msg,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
            )""",
)

with open(target, "w") as f:
    f.write(content)

print("PATCHED successfully!")

# Verify
with open(target, "r") as f:
    for i, line in enumerate(f):
        if "except TypeError" in line:
            print(f"  Found try/except at line {i + 1}")
