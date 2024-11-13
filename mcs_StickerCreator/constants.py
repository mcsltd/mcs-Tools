import enum

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3

RADIUS_REF_POINT = 3.5 * mm
A3 = A3


class Sign(enum.StrEnum):
    lot = "lot"
    sn = "sn"

