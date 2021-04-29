from curriculum_model.db.schema import Base, BoolField
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, NCHAR, String, Table, Unicode, text


ql_student = Table(
    'tt_student', Base.metadata,
    Column('student_id', CHAR(11), nullable=False),
    Column('name', String(100), nullable=False),
    Column('instrument', String(50))
)


ql_student_enrols = Table(
    'tt_student_enrols', Base.metadata,
    Column('student_id', CHAR(11), nullable=False),
    Column('aos_code', CHAR(6), nullable=False),
    Column('session', Integer, nullable=False),
    Column('acad_year', Integer, nullable=False),
    Column('score', String(10)),
    Column('stage', String(50), nullable=False),
    Column('module_code', String(15), nullable=False)
)
