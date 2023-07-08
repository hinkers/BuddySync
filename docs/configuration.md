
## Config Definitions

### Api Definitions
This is the definition of the API and any authentication to go with it.

| Key       | Required | Data Type                                              | Description                                                                           |
| --------- | -------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| auth_type | Required | Enum( "none", "apikey", "oauth1", "oauth2", "custom" ) | The type of authentication the API requires.                                          |
| base_url  | Required | String                                                 | The starting part of the URI for the API, this will be prepended to any endpoint URI. |

<!-- tabs:start -->

#### **ApiKey**
| Key             | Required | Data Type                 | Description                                                                            |
| --------------- | -------- | ------------------------- | -------------------------------------------------------------------------------------- |
| api_key         | Required | String                    | The api key to use, it is recommended to make use of `.env` variables for the api key. |
| apikey_location | Required | Enum( "param", "header" ) | When sending the api key via a URI parameter, this will be the name of the parameter.  |
| apikey_name     | Required | String                    | When sending the api key via a header, this will be the name of the header.            |

#### Example
```yaml
apis:
  - auth_type: apikey
    api_key: ${API_KEY}
    apikey_name: token
    apikey_location: param
    base_url: https://gnews.io/api/v4
```

#### **OAuth1**
| Key               | Required | Data Type | Description                                                  |
| ----------------- | -------- | --------- | ------------------------------------------------------------ |
| consumer_key      | Required | String    | The OAuth consumer key.                                      |
| consumer_secret   | Required | String    | The OAuth consumer secret.                                   |
| name              | Required | String    | A friendly name for the oauth server, e.g twitter, facebook. |
| authorize_url     | Required | String    | The URL to get an authorization token (defined by API host). |
| access_token_url  | Required | String    | The URl to get the access token (defined by API host).       |
| request_token_url | Required | String    | The URl to get the request token (defined by API host).      |

#### Example
```yaml
apis:
  - auth_type: oauth1
    consumer_key: ${API_KEY}
    consumer_secret: ${API_KEY_SECRET}
    name: Twitter
    authorize_url: https://api.twitter.com/oauth/authorize
    access_token_url: https://api.twitter.com/oauth/access_token
    request_token_url: https://api.twitter.com/oauth/request_token
    base_url: https://api.twitter.com/1.1
```

#### **OAuth2**
| Key              | Required | Data Type                | Description                                                                         |
| ---------------- | -------- | ------------------------ | ----------------------------------------------------------------------------------- |
| client_id        | Required | String                   | The OAuth client id.                                                                |
| client_secret    | Required | String                   | The OAuth client secret.                                                            |
| name             | Required | String                   | A friendly name for the oauth server, e.g twitter, facebook.                        |
| redirect_url     | Required | String                   | The redirect url that you set when creating your OAuth connection.                  |
| authorize_url    | Required | String                   | The URL to get an authorization token (defined by API host).                        |
| access_token_url | Required | String                   | The URl to get the access token (defined by API host).                              |
| response_type    | Optional | String, default = "code" | The name of the parameter that is returned in the redirect.                         |
| temp_web_server  | Optional | Boolean                  | If `True` will spin up a temporary webserver to accept the redirect OAuth response. |

#### Example
```yaml
apis:
  - auth_type: oauth2
    base_url: https://graphql.anilist.co
    client_id: ${CLIENT_ID}
    client_secret: ${CLIENT_SECRET}
    name: ${NAME}
    redirect_url: ${REDIRECT_URL}
    authorize_url: https://anilist.co/api/v2/oauth/authorize
    access_token_url: https://anilist.co/api/v2/oauth/token
    response_type: code
    temp_web_server: True
```

### **No Authentication**
#### Example
```yaml
apis:
  - auth_type: None
    base_url: https://app.fakejson.com
```

<!-- tabs:end -->

### Endpoints
Creates a named enpoint (where `<name>` is the name of the endpoint). This can be called automatically or manually through custom scripts.

| Key       | Required | Data Type                                       | Description                                                                                        |
| --------- | -------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| endpoint  | Required | String                                          | The URI for the endpoint, this will be prepended to the BaseUrl defined in the api authentication. |
| method    | Required | Enum( "GET", "POST", "PATCH", "PUT", "DELETE" ) | The http method to use for this endpoint.                                                          |
| data      | Optional | String                                          | A JSON string to send as the body of the request.                                                  |
| data_file | Optional | String                                          | The relative filepath to a JSON file that will be sent as the body of the request.                 |
| put_file  | Optional | String                                          | The relative filepath to a JSON file that will be sent as the body of the request.                 |
| params    | Optional | List(NameValuePair)                             | Will send the value of this key as URI paramter with the name `<param_name>`                       |
| headers   | Optional | List(NameValuePair)                             |                                                                                                    |

#### Example
```yaml
apis:
  - auth_type: apikey
    ...
    endpoints:
      - name: top_headlines
        endpoint: /top-headlines
        method: GET
      - name: search
        endpoint: /search
        method: GET
        params:
          - name: q
            value: example
          - name: max
            value: 5
```

### Database Definitions
The database connection information.

| Key               | Required | Data Type          | Description                                                                                                                                                              |
| ----------------- | -------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| name              | Required | String             |                                                                                                                                                                          |
| connection_string | Required | String             | The connection string for the database, for more information see the SQLAlchemy documentation [here](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls). |
| create_tables     | Optional | Boolean            | If `True` will check to see if the defined tables exist in the database and if not, will create them.                                                                    |
| relationships     | Optional | List(Relationship) |                                                                                                                                                                          |
| tables            | Optional | List(Table)        |                                                                                                                                                                          |


### Relationship Definitions
The database connection information.

| Key         | Required | Data Type    | Description |
| ----------- | -------- | ------------ | ----------- |
| one_to_one  | Optional | List(String) |             |
| one_to_many | Optional | List(String) |             |

<!-- tabs:start -->

### **One to One**
```yaml
relationships:
      one_to_one:
        - ChildTable.foriegn_key -> ParentTable.primary_key
        - Article.author_id -> Author.id
```

### **One to Many**
```yaml
relationships:
      one_to_many:
        - ChildTable.foriegn_key -> ParentTable.primary_key
        - Article.author_id -> Author.id
```

<!-- tabs:end -->

### Table Definitions
The database connection information.

| Key         | Required | Data Type    | Description |
| ----------- | -------- | ------------ | ----------- |
| name        | Required | String       |             |
| primary_key | Optional | String       |             |
| columns     | Required | List(Column) |             |

### Column Definitions
Data types match to the SQLAlchemy data types.
https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types

| Data types   | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| BigInteger   | A type for bigger `int` integers.                                  |
| Boolean      | A bool datatype.                                                   |
| Column       | A type for `datetime.date()` objects.                              |
| Date         | A type for `datetime.datetime()` objects.                          |
| DateTime     | A type for double `FLOAT` floating point types.                    |
| Float        | Generic Enum Type.                                                 |
| ForeignKey   | Type representing floating point types, such as `FLOAT` or `REAL`. |
| Integer      | A type for `int` integers.                                         |
| Interval     | A type for `datetime.timedelta()` objects.                         |
| LargeBinary  |
| Numeric      |
| SmallInteger |
| String       |
| Table        |
| Text         |
| Time         |
| Unicode      |
| UnicodeText  |

`column_name: type`