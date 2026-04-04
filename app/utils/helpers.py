from bson import ObjectId


def oid_str(oid: ObjectId) -> str:
    return str(oid)


def normalize_mongo_doc(doc: dict | None) -> dict | None:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
