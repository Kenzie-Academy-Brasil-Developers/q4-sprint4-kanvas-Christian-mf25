# Relatório de testes

Todas as atividades do trimestre possuem requisitos mínimos obrigatórios:

<section class="hilightedContet">

<header>**Importante!**</header>

O **formato dos JSONs** de todas as requisições e respostas deve coincidir com os formatos especificados nos enunciados.

As **URLs** definidas devem ser as mesmas especificadas.

Os **códigos de status HTTP** também devem ser iguais aos definidos para as atividades.

</section>

Para auxiliar na checagem desses requisitos e verificar se tudo está de acordo com essas três regras, serão disponibilizados arquivos de testes para cada atividade. Esses arquivos terão o objetivo de garantir que os requisitos mínimos obrigatórios estão sendo atendidos em seu projeto, além de auxiliar a equipe de ensino durante a correção das atividades.

Cada atividade terá um link para seu respectivo arquivo de testes. Basta adicioná-lo à raiz do seu projeto e rodar o seguinte comando:

    python manage.py test -v 2 &> report.txt

O comando executará os testes e adicionará a saída da execução num arquivo chamado `report.txt`. Esse arquivo conterá um relatório dos testes executados e seus respectivos resultados. Caso ele aponte falhas, significa que os requisitos mínimos não estão sendo totalmente cumpridos em seu projeto. Se isso acontecer, o relatório indicará o erro encontrado e apontará o que precisa ser corrigido. Você pode gerar o relatório quantas vezes achar necessário. Apenas a versão final deve ser enviada junto com os demais arquivos do projeto.

## Utilizando banco Postgres

Existe um problema quando rodamos os testes em um banco Postgres, porque ele não reseta os IDs por padrão. Para o caso dos nossos testes, isso é uma pequena dor de cabeça.

Sendo assim, caso você queira utilizar um banco Postgres em seu projeto, será necessário incluir a configuração do SQLite apenas para rodar os testes.

    # settings.py

    import os

    ...

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': <nome-do-seu-banco>,
            'USER': <nome-do-user>,
            'PASSWORD': <senha-do-user>,
            'HOST': <db-hostname-ou-ip>, # Por estar configurado localmente vai ser no localhost ou 127.0.0.1
            'PORT': <porta-do-banco> # Por padrão o PostgreSQL roda na porta 5432
        }
    }

    test = os.environ.get('TEST')

    if test:    
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

No momento de executar, é necessário incluir a variável `TEST` antes do comando.

    TEST=TEST python manage.py test -v 2 &> report.txt
