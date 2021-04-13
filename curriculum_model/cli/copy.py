import click
from curriculum_model.db import DB, table_map
from curriculum_model.db.schema import Base
from sqlalchemy.inspection import inspect


def dependency_chain(key_only=False):
    c = ['curriculum',
         'course',
         'course_config',
         'course_session',
         'course_session_config',
         'cgroup',
         'cgroup_config',
         'component',
         'cost',
         'cost_week'
         ]
    key_objects = [1, 3, 5, 7]
    if key_only:
        return [o for i, o in enumerate(c) if i in key_objects]
    else:
        return c


@click.command()
@click.argument("obj_name", type=click.Choice(dependency_chain(True)))
@click.argument("obj_id", type=int)
@click.argument("parent_id", type=int)
# @click.option("--move", "-m", is_flag=True, help="Delete the original file after copying.")
@click.pass_obj
def copy(config, obj_name, obj_id, parent_id):
    config.verbose_print(
        f"Attempting to copy {obj_name} with id {obj_id} and its sub-objects to parent with id {parent_id}.")
    dc = dependency_chain(False)
    tm = table_map(Base)
    # Get the type of object the parent is
    parent_name = dc[dc.index(obj_name)-1]
    parent_class = tm[parent_name]
    # open connection
    with DB(config.echo, config.environment) as db:
        session = db.session()
        # If the parent doesn't have a curriculum id then it's a config, so go one step further to get curriculum id
        if not hasattr(parent_class.__table__.columns, "curriculum_id"):
            grandparent_name = dc[dc.index(obj_name)-2]
            grandparent_class = tm[grandparent_name]
            base_class = grandparent_class
        else:
            base_class = parent_class
        if not click.confirm(f"Proceed with copying {obj_name} with ID {obj_id} " +
                             f"to {base_class.__tablename__} with ID {parent_id}?",
                             abort=True):
            pass
        curriculum_id = session.query(base_class).get(parent_id).curriculum_id
        parent_obj = session.query(base_class).get(parent_id)
        obj_class = tm[obj_name]
        obj = session.query(obj_class).get(obj_id)
        _recursive_copy(session, curriculum_id, parent_obj,
                        obj, tm, dc, config, 0)
        if click.confirm("Commit changes?"):
            session.commit()
        else:
            session.rollback()


def _recursive_copy(session, curriculum_id, parent_obj, child_obj, tm, dc, config, indent_level):
    indent = indent_level*"\t "
    # Columns to copy
    tbl = child_obj.__table__
    cols = [c for c in tbl.columns.keys() if c not in tbl.primary_key]
    # If no columns, it's reached cost_week (two pk columns) so add week column back in
    if len(cols) == 0:
        cols = ['acad_week', 'cost_id']
    # Convert existing record to dictionary of non-pk columns
    data = {c: getattr(child_obj, c) for c in cols}
    # Change curriculum_id value, if possible
    if 'curriculum_id' in data.keys():
        data['curriculum_id'] = curriculum_id
    # CHange the parent object ID column, if possible
    parent_pk_name = list(parent_obj.__table__.primary_key)[0].name
    if parent_pk_name in data.keys():
        data[parent_pk_name] = getattr(parent_obj, parent_pk_name)
    # GEt pk col for reference later
    child_pk_name = list(child_obj.__table__.primary_key)[0].name

    # Create new object, add to DB
    new_child_obj = child_obj.__class__(**data)
    session.add(new_child_obj)
    session.flush()
    config.verbose_print(f"{indent}Created {child_obj.__tablename__} " +
                         f"with ID {getattr(new_child_obj, child_pk_name)}")

    # add config_entry if a config exists between parent and child
    if abs(dc.index(parent_obj.__tablename__) - dc.index(new_child_obj.__tablename__)) == 2:
        config.verbose_print(
            f"{indent}Creating config link for {parent_obj.__tablename__}.")
        config_class = tm[parent_obj.__tablename__ + '_config']
        new_conf_values = {parent_pk_name: getattr(parent_obj, parent_pk_name),
                           child_pk_name: getattr(new_child_obj, child_pk_name)}
        new_conf = config_class(**new_conf_values)
        session.add(new_conf)
        session.flush()
    # Get children of child
    dc_pos = dc.index(child_obj.__tablename__)
    if dc_pos == len(dc)-1:
        # Reached final object, stop recurse
        return
    grandchild_name = dc[dc_pos+1]
    if grandchild_name[-6:] == "config":
        config.verbose_print(f"{indent}Detected config link")
        # get grandchildren using config
        config_class = tm[grandchild_name]
        grandchild_name = dc[dc.index(grandchild_name)+1]
        grandchild_class = tm[grandchild_name]
        grandchild_pk_col_name = list(
            grandchild_class.__table__.primary_key)[0].name
        grandchildren_ids_query = session.query(config_class) \
            .filter(getattr(config_class, child_pk_name)
                    == getattr(child_obj, child_pk_name))
    else:
        config.verbose_print(f"{indent}Detected direct link")
        grandchild_class = tm[grandchild_name]
        grandchild_pk_col_name = list(
            grandchild_class.__table__.primary_key)[0].name
        grandchildren_ids_query = session.query(grandchild_class) \
            .filter(getattr(grandchild_class, child_pk_name)
                    == getattr(child_obj, child_pk_name))
    grandchildren_ids = [getattr(c, grandchild_pk_col_name)
                         for c in grandchildren_ids_query.all()]
    grandchildren = session.query(grandchild_class) \
        .filter(getattr(grandchild_class, grandchild_pk_col_name).in_(grandchildren_ids))
    for grandchild_obj in grandchildren.all():
        _recursive_copy(session,
                        curriculum_id,
                        new_child_obj,
                        grandchild_obj,
                        tm,
                        dc, config, indent_level+1)
