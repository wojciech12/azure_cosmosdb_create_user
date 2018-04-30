Create cosmosdb database and Corresponding User
-----------------------------------------------

Script creates a database in cosmosdb container and a corresponding user. As output, it prints a temporary token for the user.

**Notice**: cosmosdb does not support users as you would expect in a database. You have to use your service keys (az cosmosdb get-keys --resource-group RESOURCE_GROUP --name COSMOSDB_CONTAINER) or temporary user/token. The temporary user/token will not work if you want to use the mongodb client.

::

  # az cosmosdb show --resource-group RESOURCE_GROUP --name COSMOSDB_NAME --query 'documentEndpoint' -o tsv
  export COSMOSDB_ENDPOINT= 
  # az cosmosdb list-keys --resource-group RESOURCE_GROUP --name COSMOSDB_NAME --query 'primaryMasterKey' -o tsv
  export COSMOSDB_MASTERKEY=
  export USER_NAME=
  export DB_NAME=
  
  python create_db_and_creds.py

Reference
---------

- https://docs.microsoft.com/en-us/azure/cosmos-db/secure-access-to-data#resource-tokens
- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples
- https://github.com/Azure/azure-documentdb-python/blob/master/test/query_execution_context_tests.py
- https://github.com/Azure/azure-documentdb-python/blob/master/test/crud_tests.py
- https://github.com/Azure/azure-documentdb-dotnet/blob/master/samples/code-samples/UserManagement/Program.cs
