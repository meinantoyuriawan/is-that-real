from dataclasses import dataclass
from datetime import datetime

# @dataclass
# class UserModel:
#     id: int | None
#     email: str
#     hashed_password: str
#     is_active: bool = True
#     created_at: datetime = datetime.utcnow()

#     def deactivate(self):
#         """Pure business logic rule"""
#         self.is_active = False

@dataclass
class VectorModel:
    url: str
    judul: str
    clean_text: str