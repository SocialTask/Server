## Endpoints de Usuarios

### Buscar Usuarios

- **URL**: `/search`
- **Método**: `GET`

#### Parámetros de Consulta:
- `query`: Cadena de búsqueda para encontrar usuarios

#### Respuesta:
- **Código de Respuesta Exitosa**: 200
- **Código de Respuesta de Error**: 500 (Error del Servidor)

##### Cuerpo de Respuesta Exitosa:

```json
[
    {
        "id": "<user_id>",
        "username": "<username>",
        "profile_pic_url": "<profile_picture_url>",
        "followers_count": <followers_count>,
        "following_count": <following_count>,
        "made_tasks": <made_tasks>,
        "points": <points>,
        "verified": <verified>,
        "description": "<user_description>"
    },
    {
        ...
    }
]
```

### Perfil de Usuario

- **URL**: `/user/<identifier>`
- **Método**: `GET`
- **Autorización**: Token de Acceso Requerido

#### Parámetros de Ruta:
- `identifier`: Nombre de usuario o ID de usuario

#### Parámetros de Consulta Opcionales:
- `fromid`: Indicador booleano para especificar si el identificador es un ID de usuario (`true`) o un nombre de usuario (`false`)

#### Respuesta:
- **Código de Respuesta Exitosa**: 200
- **Código de Respuesta de Error**: 404 (No Encontrado), 500 (Error del Servidor)

##### Cuerpo de Respuesta Exitosa:

```json
{
    "id": "<user_id>",
    "username": "<username>",
    "profile_pic_url": "<profile_picture_url>",
    "followers_count": <followers_count>,
    "following_count": <following_count>,
    "made_tasks": <made_tasks>,
    "points": <points>,
    "verified": <verified>,
    "description": "<user_description>"
}
```

##### Cuerpo de Respuesta de Error:

```json
{
    "error": "Failed to fetch user profile",
    "message": "Reason for failure"
}
```