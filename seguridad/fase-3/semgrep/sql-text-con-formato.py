from sqlalchemy import text


def filtrar_mal_directo(query, filter):
    # ruleid: sql-text-con-formato
    return query.filter(text("title = '%s' or content = '%s'" % (filter, filter)))


def filtrar_mal_fstring(query, filter):
    # ruleid: sql-text-con-formato
    return query.filter(text(f"title = '{filter}'"))


def filtrar_mal_variable(session, filter):
    # ruleid: sql-text-con-formato
    consulta = "title = '%s'" % filter
    return session.execute(text(consulta))


def filtrar_bien_parametros(query, filter):
    # ok: sql-text-con-formato
    return query.filter(text("title = :t or content = :t")).params(t=filter)


def filtrar_bien_orm(model, filter):
    # ok: sql-text-con-formato
    return model.query.filter(model.title.like(f"%{filter}%"))
