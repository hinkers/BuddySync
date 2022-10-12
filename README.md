# Api-Sync

## Config Definitions

### [Authentication]
This is the definition of the API and any authentication to go with it.

| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| AuthType | Required | Enum( "None", "ApiKey", "OAuth1", "OAuth2" ) | The type of authentication the API requires. |
| BaseUrl | Required | String | The starting part of the URI for the API, this will be prepended to any endpoint URI. |

#### ApiKey Authentication
| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| ApiKey | Required | String | The api key to use, it is recommended to make use of `.env` variables for the api key. |
| ParamName | Optional | String | When sending the api key via a URI parameter, this will be the name of the parameter. |
| HeaderName | Optional | String | When sending the api key via a header, this will be the name of the header. |

#### OAuth1 Authentication
| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| ConsumerKey | Required | String | The OAuth consumer key. |
| ConsumerSecret | Required | String | The OAuth consumer secret. |
| Name | Required | String | A friendly name for the oauth server, e.g twitter, facebook. |
| AuthorizeUrl | Required | String | The URL to get an authorization token (defined by API host). |
| AccessTokenUrl | Required | String | The URl to get the access token (defined by API host). |
| RequestTokenUrl | Required | String | The URl to get the request token (defined by API host). |

#### OAuth2 Authentication
| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| ClientId | Required | String | The OAuth client id. |
| ClientSecret | Required | String | The OAuth client secret. |
| Name | Required | String | A friendly name for the oauth server, e.g twitter, facebook. |
| RedirectUrl | Required | String | The redirect url that you set when creating your OAuth connection. |
| AuthorizeUrl | Required | String | The URL to get an authorization token (defined by API host). |
| AccessTokenUrl | Required | String | The URl to get the access token (defined by API host). |
| ResponseType | Optional | String, default = "code" | The name of the parameter that is returned in the redirect. |
| TempWebServer | Optional | Boolean | If `True` will spin up a temporary webserver to accept the redirect OAuth response. |

### [Endpoint:`<name>`]
Creates a named enpoint (where `<name>` is the name of the endpoint). This can be called automatically or manually through custom scripts.

| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| Endpoint | Required | String | The URI for the endpoint, this will be prepended to the BaseUrl defined in the api authentication. |
| Method | Required | Enum( "GET", "POST", "PATCH", "PUT", "DELETE" ) | The http method to use for this endpoint. |
| Param_`<param_name>` | Optional | String | Will send the value of this key as URI paramter with the name `<param_name>` |
| Data | Optional | String | A JSON string to send as the body of the request. |
| DataFile | Optional | String | The relative filepath to a JSON file that will be sent as the body of the request. |

### [SQL]
The database connection information.

| Key | Required | Data Type | Description |
| --- | --- | --- | --- |
| ConnectionString | Required | String | The connection string for the database, for more information see the SQLAlchemy documentation [here](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls). |
| CreateTables | Optional | Boolean | If `True` will check to see if the defined tables exist in the database and if not, will create them. |

### [Table:`<name>`]
The database connection information.

| Key | Required | Data Type | Description |
| --- | --- | --- | --- |