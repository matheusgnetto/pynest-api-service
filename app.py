from config import config
from nest.core.app import App
from src.facebook.facebook_module import FacebookModule

app = App(
    description="""# 📄Vamos começar?

Nossa API fornece uma série de ferramentas e recursos para facilitar a extração e manipulação de dados de clientes vinculados na plataforma Mediahub V4.

---

# **Guia de Introdução**

### Como gero meu token?

Para começar a usar nossa API, você precisa seguir os passos abaixo:

Acessar [https://mktlab.app/](https://mktlab.app/)
Fazer login usando o SSO da v4company.  
Navegar até Rede > Clientes > Mediahub > Extração de Dados > Token ID e clicar em "Gerar". O token gerado será copiado para sua área de transferência.  
Usar o token no cabeçalho da requisição como "Authorization".

##### **Notas:**

- A API tem limites de taxa e uso.
- A API só responde a comunicações seguras via HTTPS.
- A API retorna respostas de solicitação no formato JSON.
    

## Authentication

A API usa tokens de autorização para autenticação. Você deve incluir um token de autorização em cada solicitação à API com o cabeçalho Authorization.

#### Resposta de Erro de Autenticação

Se um token de autorização estiver faltando, malformado ou inválido, você receberá um código de resposta HTTP 401 Não Autorizado.

## Limites de Taxa e Uso

O limite é de 1000 solicitações por minuto.  
A paginação é realizada a cada 500 registros (podendo ser alterado sem aviso prévio conforme demanda).

### 503 response

Uma resposta HTTP 503 indica um pico inesperado no tráfego de acesso à API.
""", modules=[FacebookModule], title="Mediahub Application"
)


@app.on_event("startup")
async def startup():
    await config.create_all()
