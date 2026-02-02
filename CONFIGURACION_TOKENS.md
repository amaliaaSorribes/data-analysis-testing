# Configuración de Tokens de API

Este proyecto soporta dos proveedores de IA:

## OpenAI
Para usar OpenAI, configura en tu archivo `.env`:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...tu_token_aqui
```

## GitHub Models
Para usar GitHub Models (gratis con tu cuenta de GitHub), configura:
```env
AI_PROVIDER=github
GITHUB_TOKEN=ghp_...tu_token_aqui
```

### Cómo obtener un token de GitHub:
1. Ve a https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre y selecciona los scopes necesarios
4. Copia el token y ponlo en tu archivo `.env`

### Modelos disponibles:
- **OpenAI**: gpt-4o-mini (por defecto)
- **GitHub**: gpt-4o (por defecto)

## Configuración inicial:
1. Copia `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edita `.env` con tus credenciales
3. El sistema usará automáticamente el proveedor configurado
