# User verisini çek - QUERY
```graphql
query {
  user(id: 1) {
    id
    name
    email
  }
}
```
#  User'ı güncelle - MUTATION
```graphql
mutation {
  updateUser(id: 1, name: "Yeni İsim") {
    id
    name
  }
}

```
#  User'ı sil - MUTATION
```graphql
mutation {
  deleteUser(id: 1) {
    ok
  }
}

```

## Introspection ile bütün verileri görelim

```graphql
query {
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}

```

<details>
  <summary>Introspection Output</summary>


```
{
  "data": {
    "__schema": {
      "types": [
        {
          "name": "Query",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": "Node"
              }
            },
            {
              "name": "user",
              "type": {
                "name": "UsersConnection"
              }
            },
            {
              "name": "bug",
              "type": {
                "name": "BugsConnection"
              }
            },
            {
              "name": "findUser",
              "type": {
                "name": "Users"
              }
            },
            {
              "name": "findBug",
              "type": {
                "name": "Bugs_"
              }
            },
            {
              "name": "allUsers",
              "type": {
                "name": "UsersConnection"
              }
            },
            {
              "name": "allBugs",
              "type": {
                "name": "BugsConnection"
              }
            }
          ]
        },
        {
          "name": "Node",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "ID",
          "fields": null
        },
        {
          "name": "UsersConnection",
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "PageInfo",
          "fields": [
            {
              "name": "hasNextPage",
              "type": {
                "name": null
              }
            },
            {
              "name": "hasPreviousPage",
              "type": {
                "name": null
              }
            },
            {
              "name": "startCursor",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "endCursor",
              "type": {
                "name": "String"
              }
            }
          ]
        },
        {
          "name": "Boolean",
          "fields": null
        },
        {
          "name": "String",
          "fields": null
        },
        {
          "name": "UsersEdge",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": "Users"
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "Users",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null
              }
            },
            {
              "name": "username",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "bugs",
              "type": {
                "name": "Bugs_Connection"
              }
            }
          ]
        },
        {
          "name": "Bugs_Connection",
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "Bugs_Edge",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": "Bugs_"
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "Bugs_",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null
              }
            },
            {
              "name": "reporterId",
              "type": {
                "name": "Int"
              }
            },
            {
              "name": "text",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "private",
              "type": {
                "name": "Boolean"
              }
            },
            {
              "name": "reporter",
              "type": {
                "name": "Users"
              }
            }
          ]
        },
        {
          "name": "Int",
          "fields": null
        },
        {
          "name": "BugsConnection",
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "BugsEdge",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": "Bugs"
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "Bugs",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null
              }
            },
            {
              "name": "reporterId",
              "type": {
                "name": "Int"
              }
            },
            {
              "name": "private",
              "type": {
                "name": "Boolean"
              }
            },
            {
              "name": "reporter",
              "type": {
                "name": "Users"
              }
            }
          ]
        },
        {
          "name": "__Schema",
          "fields": [
            {
              "name": "types",
              "type": {
                "name": null
              }
            },
            {
              "name": "queryType",
              "type": {
                "name": null
              }
            },
            {
              "name": "mutationType",
              "type": {
                "name": "__Type"
              }
            },
            {
              "name": "subscriptionType",
              "type": {
                "name": "__Type"
              }
            },
            {
              "name": "directives",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "__Type",
          "fields": [
            {
              "name": "kind",
              "type": {
                "name": null
              }
            },
            {
              "name": "name",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "fields",
              "type": {
                "name": null
              }
            },
            {
              "name": "interfaces",
              "type": {
                "name": null
              }
            },
            {
              "name": "possibleTypes",
              "type": {
                "name": null
              }
            },
            {
              "name": "enumValues",
              "type": {
                "name": null
              }
            },
            {
              "name": "inputFields",
              "type": {
                "name": null
              }
            },
            {
              "name": "ofType",
              "type": {
                "name": "__Type"
              }
            }
          ]
        },
        {
          "name": "__TypeKind",
          "fields": null
        },
        {
          "name": "__Field",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "args",
              "type": {
                "name": null
              }
            },
            {
              "name": "type",
              "type": {
                "name": null
              }
            },
            {
              "name": "isDeprecated",
              "type": {
                "name": null
              }
            },
            {
              "name": "deprecationReason",
              "type": {
                "name": "String"
              }
            }
          ]
        },
        {
          "name": "__InputValue",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "type",
              "type": {
                "name": null
              }
            },
            {
              "name": "defaultValue",
              "type": {
                "name": "String"
              }
            }
          ]
        },
        {
          "name": "__EnumValue",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "isDeprecated",
              "type": {
                "name": null
              }
            },
            {
              "name": "deprecationReason",
              "type": {
                "name": "String"
              }
            }
          ]
        },
        {
          "name": "__Directive",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String"
              }
            },
            {
              "name": "locations",
              "type": {
                "name": null
              }
            },
            {
              "name": "args",
              "type": {
                "name": null
              }
            }
          ]
        },
        {
          "name": "__DirectiveLocation",
          "fields": null
        }
      ]
    }
  }
}
```
</details>
