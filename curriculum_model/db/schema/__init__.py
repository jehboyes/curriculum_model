# coding: utf-8
"""Tables used in the curriculum model. Other key schema objects are stored in sub-modules. """
from sqlalchemy import CHAR, Column, DECIMAL, Date, BOOLEAN, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, NCHAR, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeMeta
import sys
import inspect

Base = declarative_base()


BoolField = BOOLEAN()


class parameter(Base):
    __tablename__ = '_parameter'

    parameter = Column(String(100), primary_key=True)
    value = Column(String(100))


class aos_code(Base):
    """
    An area of study.

    Used Matches the code used in the student record system.
    """
    __tablename__ = 'aos_code'

    aos_code = Column(CHAR(6), primary_key=True,
                      comment="6 character unique identifier.")
    description = Column(String(50), comment="Name of the area of study.")
    fee_cat_id = Column(String(20), ForeignKey("fee_category.fee_cat_id"))
    department_id = Column(NCHAR(3), ForeignKey("department.department_id"))
    pathway = Column(String(50), comment="Alternative to description field.")
    valid_for_projection = Column(
        BoolField, comment="Flag for inclusion in future projection exercises.")
    require_foundation = Column(
        BoolField, comment="Flag for whether the area of study includes a foundation year.")


class Calendar(Base):
    """
    A type of calendar.
    """
    __tablename__ = 'calendar'

    calendar_type = Column(Unicode(20), primary_key=True,
                           comment="Unique identifier for calendar type.")
    long_description = Column(Unicode(
        200), nullable=False, comment="Detailed description of the calendar type.")
    epoch_name = Column(
        Unicode(20), comment="Name of the calendar blocks (e.g. 'term')")


class CgroupStrand(Base):
    """
    A strand to which the component group belongs.
    """
    __tablename__ = 'cgroup_strand'

    strand_id = Column(String(5), primary_key=True,
                       comment="Unique identifier for the strand.")
    description = Column(String(30), nullable=False,
                         comment="Description of the stand.")


class ComponentStaffing(Base):
    """
    Level of staffing on a component.

    Discrete levels of staffing, according to the number of different staff working on the component.
    Bands shouldn't overlap.
    """
    __tablename__ = 'component_staffing'

    band_id = Column(Integer, primary_key=True,
                     comment="Unique identifier for the staffing band.")
    description = Column(String(50), nullable=False,
                         comment="Description of the band (should state the interval).")
    multiplier = Column(DECIMAL(10, 5), nullable=False,
                        comment="Multiplier used in the calculation of module coordination.")


class CostType(Base):
    """
    A category for the cost.

    Used to modify the resource requirements of costs, and
    to decide which costs are timetabled.
    """
    __tablename__ = 'cost_type'

    cost_type = Column(String(20), primary_key=True,
                       comment="Unique identifier for the cost type.")
    cost_multiplier = Column(Float(53), nullable=False,
                             server_default=text("((1))"), comment="Decimal multiplier by which the minutes or value of the cost are multiplied.")
    is_pay = Column(BoolField, nullable=False,
                    comment="If the cost relates to pay.")
    is_contact = Column(BoolField, nullable=False,
                        comment="If the cost is staff-student contact time.")
    nominal_account = Column(
        Integer, nullable=False, comment="The general ledger account that thiscost type defaults to.")
    is_assessing = Column(BoolField, comment="If the cost is an assesment.")
    is_assignment = Column(
        BoolField, comment="If the cost is an assignment, i.e. invokes 'script' marking.")
    is_taught = Column(BoolField, comment="If the cost is teaching.")


class CostTypePay(Base):
    """
    Provides description for the cost_type is_pay flag.
    """
    __tablename__ = 'cost_type_pay'

    is_pay = Column(BoolField, primary_key=True,
                    comment="True or false for pay or nonpay respectively.")
    description = Column(String(30), nullable=False,
                         comment="Verbose description like 'pay' or 'non-pay'.")


class Costc(Base):
    """
    A cost centre, or 'budget code'.
    """
    __tablename__ = 'costc'

    costc = Column(CHAR(6), primary_key=True,
                   comment="Unique identifier for a cost centre.")
    description = Column(String(50), nullable=False,
                         comment="Description of the cost centre.")
    pathway = Column(BoolField, nullable=False,
                     comment="Alternative to description.")
    primary_aos_code = Column(CHAR(6), ForeignKey("aos_code.aos_code"))
    department_id = Column(
        CHAR(1), ForeignKey("department.department_id"))


class Department(Base):
    """
    A school or department.

    Usually a parent object for areas of study, or cost centre.
    """
    __tablename__ = 'department'

    department_id = Column(NCHAR(3), primary_key=True,
                           comment="Unique identifier for the department.")
    description = Column(String(50), nullable=False,
                         comment="Short description of the department.")
    long_description = Column(
        String(50), nullable=False, comment="Formal title of the Department.")


class FeeCategory(Base):
    """
    A high-level category of fee.
    """
    __tablename__ = 'fee_category'

    fee_cat_id = Column(String(20), primary_key=True,
                        comment="Unique identifier for the category.")
    description = Column(NCHAR(10), nullable=False,
                         comment="Description of the category.")


class FeeStatus(Base):
    """
    A low-level student fee status.

    Usually corresponds to a type of domicile.
    """
    __tablename__ = 'fee_status'

    fee_status_id = Column(String(20), primary_key=True,
                           comment="Unique identifier for the fee status. Should match SRS.")
    status_description = Column(
        String(50), nullable=False, comment="Description of the status.")
    home_overseas = Column(CHAR(1), ForeignKey("fee_category.fee_cat_id"))


class HecosCode(Base):
    """
    Higher Education Classification of Subject.
    """
    __tablename__ = 'hecos_code'

    hecos = Column(Integer, primary_key=True,
                   comment="Identifier for the classification.")
    code_name = Column(String(100), nullable=False,
                       comment="Description of the classification.")


class Module(Base):
    """
    A sub-category of component.

    Should exist for each credit-bearing component.
    """
    __tablename__ = 'module'

    module_code = Column(String(9), primary_key=True,
                         comment="Unique identifier for the module. Should match SRS.")
    credits = Column(
        Integer, comment="Number of credits awarded upon successful completion.")
    description = Column(String(100), comment="Description of the module.")


class RoomType(Base):
    __tablename__ = 'room_type'

    room_type = Column(String(20), primary_key=True,
                       comment="Unique identifier for the room_type. Is descriptive.")
    average_sq_metre = Column(Integer, server_default=text(
        "(NULL)"), comment="Average size of this room type, in square meters.")
    on_campus = Column(
        BoolField, comment="If the room is on campus, i.e. creates a space requirement.")


class SNOriginConfig(Base):
    """
    Valid combinations of origins and set categories.
    """
    __tablename__ = 'student_number_origin_config'

    origin = Column(String(50),
                    primary_key=True, nullable=False)
    set_cat_id = Column(CHAR(3),
                        primary_key=True, nullable=False)


class SNUsage(Base):
    """
    What the student numbers are used for.
    """
    __tablename__ = 'student_number_usage'

    usage_id = Column(String(20), primary_key=True,
                      comment="Unique identifier for the usage.")
    description = Column(String(200), comment="Description of the use.")
    surpress_all = Column(BoolField, server_default=text(
        "((0))"), comment="If this usage should be hidden in reporting.")
    set_cat_id = Column(CHAR(3))


class Change(Base):
    """
    A request to change the system. 
    """
    __tablename__ = 'tt_change'

    tt_change_id = Column(Integer, primary_key=True,
                          comment="Unique identifier.")
    date_created = Column(Date, nullable=False,
                          comment="Date the change was requested.")
    category = Column(String(50), nullable=False,
                      comment="Rough categorisation of the change.")
    screen = Column(
        String(50), comment="Screen of the app which would primarily be affected.")
    requested_by = Column(
        String(100), comment="User that requested the change.")
    description = Column(
        String(8000), nullable=False, comment="Verbose description of what should be changed.")
    progress = Column(String(
        8000), comment="Feedback and explanation of any progress made (or not made).")
    closed = Column(BoolField, nullable=False, server_default=text(
        "((0))"), comment="If the request is either complete or cancelled")
    closed_date = Column(Date, comment="Date the request was closed.")
    closed_version = Column(
        NCHAR(10), comment="The version of the app in which the change was closed.")
    suspend = Column(BoolField, server_default=text("((0))"),
                     comment="If the field has been 'parked'.")


class Instrument(Base):
    """
    A type of instrument.

    Exists to map several similar instrument names to shorter versions.
    """
    __tablename__ = 'tt_instrument'

    instrument = Column(String(50), primary_key=True,
                        comment="Long name of the instrument.")
    short_instrument = Column(
        String(50), comment="Shortened name of the instrument, or instrument group.")


class Stage(Base):
    """
    The stage of an enrolment, or application.
    """
    __tablename__ = 'tt_stage'

    stage = Column(String(50), primary_key=True,
                   comment="Unique identifer for the stage.")
    is_pending = Column(BoolField, nullable=False,
                        comment="If the stage is not yet a committed enrolment.")


class tt_Type(Base):
    __tablename__ = 'tt_type'

    tt_type_id = Column(Integer, primary_key=True)
    description = Column(String(20), nullable=False)


class Week(Base):
    """
    Mapper to take celcat weeks to financial periods.

    Used for accurate temporal costing of non-contractual costs.
    """
    __tablename__ = 'week'

    celcat_week = Column(Integer, primary_key=True,
                         comment="Unique numebr for the week in Celcat.")
    period = Column(Integer, nullable=False,
                    comment="Financial period to which the week belongs. ")


class CourseSession(Base):
    """
    A year of study, in a given course.
    """
    __tablename__ = 'course_session'

    course_session_id = Column(
        Integer, primary_key=True, comment="Unique identifier for the course session.")
    session = Column(Integer, nullable=False, server_default=text(
        "((1))"), comment="The enumerated year of study.")
    costc = Column(ForeignKey('costc.costc'))
    description = Column(String(100), nullable=False,
                         comment="Description of the year of study. Not to include session.")
    level = Column(Integer, nullable=True,
                   comment="Qualification level of study (*not* level of final qualification).")
    notes = Column(Unicode, server_default=text("(NULL)"),
                   comment="Additional notes on the course session.")
    curriculum_id = Column(
        Integer, comment="The curriculum to which the course_session belongs.")


class Curriculum(Base):
    """
    A specification of curriculum delivery.
    """
    __tablename__ = 'curriculum'
    __table_args__ = (
        Index('IX_curriculum', 'acad_year', 'usage_id'),
    )

    curriculum_id = Column(Integer, primary_key=True,
                           comment="Unique identifier for the curriculum.")
    description = Column(String(100), nullable=False,
                         comment="Description of the curriculum (likely to be 'Main Curriculum').")
    created_date = Column(DateTime, nullable=False,
                          comment="When the curriculum was created.")
    acad_year = Column(Integer, nullable=False,
                       comment="The academic year in whic hthe curriculum runs.")
    usage_id = Column(ForeignKey('student_number_usage.usage_id'))
    can_edit = Column(BoolField, server_default=text("((1))"),
                      comment="If the contens of the curriculum can be edited.")


class Course(Base):
    """
    A set of course sessions. 
    """
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True,
                       comment="Unique identifier for the course.")
    aos_code = Column(CHAR(6), ForeignKey("aos_code.aos_code"))
    pathway = Column(String(50), nullable=False,
                     comment="Description of the course, or major pathway if combined.")
    combined_with = Column(
        String(50), comment="Optional - name of the minor pathway, if combined.")
    award = Column(String(10), comment="Short name of the final award.")
    curriculum_id = Column(ForeignKey("curriculum.curriculum_id"))

    def __repr__(self):
        return f"{self.course_id}-{self.pathway}: from curriculum {self.curriculum_id}"


class Fee(Base):
    """
    A course fee, unique to year, category, status and session.  
    """
    __tablename__ = 'fee'

    acad_year = Column(Integer, primary_key=True,
                       nullable=False, comment="Academic year.")
    fee_cat_id = Column(ForeignKey('fee_category.fee_cat_id'),
                        primary_key=True, nullable=False)
    fee_status_id = Column(ForeignKey(
        'fee_status.fee_status_id'), primary_key=True, nullable=False)
    session = Column(Integer, primary_key=True,
                     nullable=False, comment="Year of study.")
    gross_fee = Column(DECIMAL(10, 2), nullable=False,
                       comment="Gross fee, before any waivers.")
    waiver = Column(
        DECIMAL(10, 2), comment="Reduction to fee that will be universally applied. ")


class SNInstance(Base):
    """
    An instance of a set of student numbers. 
    """
    __tablename__ = 'student_number_instance'

    instance_id = Column(Integer, primary_key=True,
                         comment="Unique identifier for the instance.")
    acad_year = Column(Integer, nullable=False, comment="Academic year.")
    usage_id = Column(ForeignKey(
        'student_number_usage.usage_id'), nullable=False)
    input_datetime = Column(DateTime, server_default=text(
        "(getdate())"), comment="When the instance was created.")
    lcom_username = Column(
        String(50), comment="Login name of the user that created the instance.")
    surpress = Column(BoolField, nullable=False, server_default=text(
        "((0))"), comment="If the instance should be hidden from reporting.")
    costc = Column(ForeignKey('costc.costc'))


class CalendarMap(Base):
    """
    Mapping weeks from an academic calendar in to actual celcat weeks. 
    """
    __tablename__ = 'calendar_map'

    acad_week = Column(Integer, primary_key=True, nullable=False,
                       comment="Week of the academic calendar.")
    curriculum_id = Column(ForeignKey(
        'curriculum.curriculum_id'), primary_key=True, nullable=False)
    term = Column(Integer, nullable=False,
                  comment="Epoch to which the week belongs.")
    description = Column(
        Unicode(50), comment="Optional field for any special name of the week.")
    calendar_type = Column(ForeignKey(
        'calendar.calendar_type'), primary_key=True, nullable=False)
    celcat_week = Column(ForeignKey('week.celcat_week'), nullable=False)


class CGroup(Base):
    """
    A group of mutually exclusive components. 
    """
    __tablename__ = 'cgroup'

    cgroup_id = Column(Integer, primary_key=True,
                       comment="Unique identifier for the component group.")
    description = Column(String(200), nullable=False,
                         comment="Description of the component group.")
    strand = Column(ForeignKey('cgroup_strand.strand_id'),
                    nullable=False, server_default=text("('MISC')"))
    notes = Column(String(8000), comment="Notes about the compoennt group.")
    curriculum_id = Column(ForeignKey('curriculum.curriculum_id'))


class Component(Base):
    """
    Similar to a module, a collection of costs. 
    """
    __tablename__ = 'component'

    component_id = Column(Integer, primary_key=True,
                          comment="Unique identifier for the component.")
    description = Column(Unicode(200), nullable=False,
                         comment="Description of the component.")
    module_code = Column(
        String(9), comment="Module code for matching back to student data.")
    calendar_type = Column(ForeignKey(
        'calendar.calendar_type'), nullable=False)
    coordination_eligible = Column(
        BoolField, nullable=False, comment="If the component should incur the additional Module Coordination cost.")
    hecos = Column(ForeignKey('hecos_code.hecos'))
    staffing_band = Column(Integer, ForeignKey('component_staffing.band_id'))
    curriculum_id = Column(ForeignKey('curriculum.curriculum_id'))


class SN(Base):
    """
    A student number in an instance, with several aggregations. 
    """
    __tablename__ = 'student_number'

    instance_id = Column(ForeignKey(
        'student_number_instance.instance_id'), primary_key=True, nullable=False)
    fee_status_id = Column(ForeignKey(
        'fee_status.fee_status_id'), primary_key=True, nullable=False)
    origin = Column(String(50),
                    primary_key=True, nullable=False, comment="Where the student numbers come from.")
    aos_code = Column(ForeignKey('aos_code.aos_code'),
                      primary_key=True, nullable=False)
    session = Column(Integer, primary_key=True,
                     nullable=False, comment="Year of study; should match sessions in course_session.")
    student_count = Column(DECIMAL(10, 5), nullable=False,
                           comment="Number of students.")


class CGroupConfig(Base):
    """
    Define membership of component_group. 
    """
    __tablename__ = 'cgroup_config'

    cgroup_id = Column(ForeignKey('cgroup.cgroup_id'),
                       primary_key=True, nullable=False, index=True)
    component_id = Column(ForeignKey('component.component_id'),
                          primary_key=True, nullable=False)
    ratio = Column(Integer, nullable=False, server_default=text(
        "((1))"), comment="Number to control prediction of relative enrolment of students within the component group.")


class Cost(Base):
    """
    An instance of curriculum delivery. 
    """
    __tablename__ = 'cost'

    cost_id = Column(Integer, primary_key=True,
                     comment="Unique identifier for the cost.")
    component_id = Column(ForeignKey(
        'component.component_id'), nullable=False,)
    room_type = Column(ForeignKey('room_type.room_type'))
    cost_type = Column(ForeignKey('cost_type.cost_type'), nullable=False)
    description = Column(String(200), nullable=False,
                         comment="Description of the cost.")
    max_group_size = Column(
        Integer, nullable=False, comment="Maximum number of students in a group; variable in calculating the number of groups required.")
    mins_per_group = Column(
        Integer, nullable=False, comment="Number of minutes delivered per group per week. Only used if the cost type is pay.")
    cost_per_group = Column(
        Integer, nullable=False, comment="Financial cost per group per week. Only used if the cost type is non-pay.")
    notes = Column(String(8000), comment="Notes about the cost.")
    number_of_staff = Column(DECIMAL(
        5, 2), comment="Number of staff required to deliver the cost (per group per week). Only used if the cost type is pay.")
    tt_type = Column(Integer, server_default=text("((1))"))
    unit_cost = Column(Integer, nullable=False, server_default='0',
                       comment="Number of minutes delivered if pay or financial cost if non pay, per group per week.")


class CostWeek(Base):
    """
    Which academic weeks that a cost runs. 
    """
    __tablename__ = 'cost_week'

    cost_id = Column(ForeignKey('cost.cost_id'),
                     primary_key=True, nullable=False)
    acad_week = Column(Integer, primary_key=True, nullable=False)


class TGroup(Base):
    """
    A group of students to be timetabled together. 
    """
    __tablename__ = 'tt_tgroup'

    tgroup_id = Column(Integer, primary_key=True,
                       comment="Unique identifier for the group.")
    cost_id = Column(ForeignKey('cost.cost_id'), nullable=False)
    notes = Column(String(
        255), comment="Notes for the benefit of either academic staff or timetabling staff.")
    room_type = Column(ForeignKey('room_type.room_type'))


class TGroupMember(Base):
    """
    Membership of a timetabling group. 
    """
    __tablename__ = 'tt_tgroup_membership'

    tgroup_id = Column(ForeignKey('tt_tgroup.tgroup_id'),
                       primary_key=True, nullable=False)
    student_id = Column(CHAR(11),
                        primary_key=True, nullable=False, comment="Un-enforced foreign key to student list.")


class TGroupStaffing(Base):
    """
    How staff are assigned to a group. 
    """
    __tablename__ = 'tt_tgroup_staffing'

    tgroup_id = Column(ForeignKey('tt_tgroup.tgroup_id'),
                       primary_key=True, nullable=False)
    staff_id = Column(String(50),
                      primary_key=True, nullable=False, comment="Unique identifier for a member of staff.")


class CourseConfig(Base):
    """
    Configuring the course to course_session relationships. 
    """
    __tablename__ = 'course_config'
    course_id = Column(Integer(), ForeignKey('course.course_id'),
                       primary_key=True, nullable=False)
    course_session_id = Column(Integer(), ForeignKey('course_session.course_session_id'),
                               primary_key=True, nullable=False)


class CourseSessionConfig(Base):
    """
    Configure the course_session to component group relationship. 
    """
    __tablename__ = 'course_session_config'
    course_session_id = Column(Integer(), ForeignKey('course_session.course_session_id'),
                               primary_key=True, nullable=False)
    cgroup_id = Column(Integer(), ForeignKey('cgroup.cgroup_id'),
                       primary_key=True, nullable=False)


tbl_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

classname_to_tablename = {name: tbl.__tablename__ for name,
                          tbl in tbl_classes if hasattr(tbl, "__tablename__")}
tablename_to_classname = {v: k for k, v in classname_to_tablename.items()}


# Build docstrings for all objects using columns
s = " "*4
for name, tbl in tbl_classes:
    if hasattr(tbl, "__tablename__"):
        cols = [getattr(tbl, c) for c in dir(tbl) if c[0] !=
                '_' and isinstance(getattr(tbl, c), InstrumentedAttribute)]
        attrs = []
        for col in cols:
            if len(col.foreign_keys) > 0:
                fk_table = str(list(col.foreign_keys)[0]).split(
                    '\'')[1].split('.')[0]
                fk_table = tablename_to_classname[fk_table]
                desc = f"**[FK]** See :py:class:`curriculum_model.db.schema.{fk_table}`."
            else:
                desc = col.comment
            if col.primary_key:
                desc = "**[PK]** " + str(desc)
            attrs += f"\n{s}{col.name} : {col.type}\n{s*2}{desc}"
            col.desc = desc
        if tbl.__doc__ is None:
            tbl.__doc__ = "Description missing"
        if tbl.__doc__[0] != '\n':
            tbl.__doc__ = '\n' + tbl.__doc__
        tbl.__doc__ = f"{s}:Name in DB: ``{tbl.__tablename__}``\n{tbl.__doc__}\n\n{s}Attributes\n{s}{10*'-'}{''.join(attrs)}"
