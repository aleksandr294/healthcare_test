from typing import Any

from django.db.models import Field, Lookup


@Field.register_lookup
class ILike(Lookup):
    lookup_name = "ilike"

    def as_sql(self, compiler: Any, connection: Any) -> tuple[str, list[str]]:
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        rhs_params = [f"%{param}%" for param in rhs_params]

        params = lhs_params + rhs_params
        return f"{lhs} ILIKE {rhs}", params
