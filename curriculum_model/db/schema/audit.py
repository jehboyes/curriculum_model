from curriculum_model.db.schema import Base, BoolField
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, NCHAR, String, Table, Unicode, text


t_audit_cgroup = Table(
    'audit_cgroup', Base.metadata,
    Column('cgroup_id', Integer, nullable=False),
    Column('description', String(200), nullable=False),
    Column('strand', String(5), nullable=False),
    Column('notes', String(200)),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


class Audit(Base):
    __tablename__ = 'tt_audit'

    username = Column(String(100), nullable=False)
    datestamp = Column(DateTime, nullable=False)
    action = Column(String(50), nullable=False)
    cost_id = Column(Integer)
    group_id = Column(Integer)
    staff_id = Column(String(50))
    student_id = Column(CHAR(11))
    actioned = Column(BoolField, server_default=text("((0))"))
    audit_id = Column(Integer, primary_key=True)


class AuditAction(Base):
    __tablename__ = 'tt_audit_action'

    action = Column(String(50), primary_key=True)
    detail_level = Column(String(50), nullable=False)


t_audit_component = Table(
    'audit_component', Base.metadata,
    Column('component_id', Integer),
    Column('description', Unicode(200)),
    Column('module_code', String(9)),
    Column('calendar_type', Unicode(20)),
    Column('coordination_eligible', BoolField),
    Column('hecos', Integer),
    Column('staffing_band', Integer),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_cost = Table(
    'audit_cost', Base.metadata,
    Column('cost_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('room_type', String(20)),
    Column('cost_type', String(20), nullable=False),
    Column('description', String(200), nullable=False),
    Column('max_group_size', Integer, nullable=False),
    Column('mins_per_group', Integer, nullable=False),
    Column('cost_per_group', Integer, nullable=False),
    Column('notes', String(8000)),
    Column('number_of_staff', DECIMAL(5, 2)),
    Column('tt_type', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_course = Table(
    'audit_course', Base.metadata,
    Column('course_id', Integer, nullable=False),
    Column('aos_code', CHAR(6)),
    Column('pathway', String(50), nullable=False),
    Column('combined_with', String(50)),
    Column('award', String(10)),
    Column('notes', String(8000)),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_course_session = Table(
    'audit_course_session', Base.metadata,
    Column('course_session_id', Integer, nullable=False),
    Column('session', Integer, nullable=False),
    Column('costc', CHAR(6)),
    Column('description', String(100), nullable=False),
    Column('notes', Unicode),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_relationships = Table(
    'audit_relationships', Base.metadata,
    Column('tbl', String(50), nullable=False),
    Column('lcom_username', String(50), nullable=False),
    Column('cmd', String(20), nullable=False),
    Column('datestamp', DateTime, nullable=False),
    Column('parent', Integer, nullable=False),
    Column('child', Integer, nullable=False)
)
