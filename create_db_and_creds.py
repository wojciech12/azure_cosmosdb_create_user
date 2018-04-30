import pydocumentdb.document_client as document_client
import os
import pydocumentdb.documents as documents


def find_database(client, named_id):

    databases = list(client.QueryDatabases({
        "query": "SELECT * FROM r WHERE r.id=@id",
        "parameters": [
            {"name": "@id", "value": named_id}
        ]
    }))

    if len(databases) > 0:
        return [databases[0]]
    else:
        return []


def get_db_link(named_id):
    return 'dbs/' + named_id


def get_user_link(named_dbid, named_id):
    return get_db_link(named_dbid) + '/users/' + named_id


if __name__ == "__main__":

    # export COSMOSDB_ENDPOINT=$(az cosmosdb show --resource-group RESOURCE_GROUP --name COSMOSDB_NAME --query 'documentEndpoint' -o tsv)
    endpoint = os.environ['COSMOSDB_ENDPOINT']

    # export COSMOSDB_MASTERKEY=$(az cosmosdb list-keys --resource-group RESOURCE_GROUP --name COSMOSDB_NAME --query 'primaryMasterKey' -o tsv)
    key = os.environ['COSMOSDB_MASTERKEY']

    mgo_user = os.environ['USER_NAME']

    mgo_db_name = os.environ['DB_NAME']

    # Initialize the Python DocumentDB client
    client = document_client.DocumentClient(endpoint, {'masterKey': key})

    # deletion for name based db
    # for name based databases
    # r = client.DeleteDatabase('dbs/' + mgo_db_name)
    # print(r)

    if len(find_database(client, mgo_db_name)) == 0:
        db = client.CreateDatabase({"id": mgo_db_name})
    else:
        print("Database " + mgo_db_name + " exists")

    db_link = get_db_link(mgo_db_name)
    db = client.ReadDatabase(db_link)

    # if you want to delete the user
    # client.DeleteUser(get_user_link(mgo_db_name, mgo_user))
    user = client.CreateUser(get_db_link(mgo_db_name), {'id': mgo_user})

    permission_definition = {
        'id': mgo_user + " all permission for all collections in" + mgo_db_name,
        'permissionMode': documents.PermissionMode.All,
        'resource': db_link + '/colls/*'
    }

    all_permission = client.CreatePermission(
        get_user_link(mgo_db_name, mgo_user),
        permission_definition)

    print(all_permission['_token'])
